import ast
import json
import logging
import re

from app.core.config import get_settings
from app.providers.llm.base_llm_provider import BaseLLMProvider
from app.providers.llm.local_provider import LocalLLMProvider
from app.schemas.critic_schema import CriticDirectiveSchema
from app.utils.text_quality import clean_final_copy, has_internal_notes, has_placeholder_text

logger = logging.getLogger(__name__)


class GroqProvider(BaseLLMProvider):
    name = "groq"
    BANNED_PHRASES = (
        "revolutionize your life",
        "unlock your potential",
        "take it to the next level",
        "cutting-edge",
        "game-changing",
        "innovative solution",
        "smarter way to interact",
        "create and innovate",
        "seamless experience",
        "empower your journey",
        "transform your world",
    )

    def __init__(self, api_key: str, model: str) -> None:
        settings = get_settings()
        self.api_key = api_key
        self.model = model
        self.fallback = LocalLLMProvider()
        self.last_provider_name = self.name
        self.last_model_name = self.model
        self.allow_fallback = bool(settings.allow_llm_fallback)
        self.max_retries = max(0, int(settings.groq_max_retries))
        from groq import Groq

        self.client = Groq(api_key=api_key, timeout=settings.groq_timeout_seconds)

    def generate_variants(
        self,
        source_text: str,
        content_type: str,
        tone: str,
        platform: str,
        count: int,
        brand_terms: list[str] | None = None,
        directives: list[CriticDirectiveSchema] | None = None,
    ) -> list[str]:
        self.last_provider_name = self.name
        self.last_model_name = self.model
        if self.client is None:
            return self._fallback_variants(source_text, content_type, tone, platform, count, brand_terms, directives)

        prompt = self._build_prompt(source_text, content_type, tone, platform, count, brand_terms, directives)
        try:
            variants = self._request_variants(prompt, count)
            if len(variants) < count:
                retry_prompt = (
                    f"{prompt}\n\n"
                    f"Retry requirement: return exactly {count} JSON string items. "
                    "Every item must be distinct, final user-facing copy, and contain no labels."
                )
                variants = self._merge_unique(variants, self._request_variants(retry_prompt, count), count)
            if len(variants) < count:
                variants = self._merge_unique(
                    variants,
                    self.fallback.generate_variants(
                        source_text=source_text,
                        content_type=content_type,
                        tone=tone,
                        platform=platform,
                        count=count,
                        brand_terms=brand_terms,
                        directives=directives,
                    ),
                    count,
                )
            if variants:
                self.last_provider_name = self.name
                self.last_model_name = self.model
                return variants[:count]
            logger.warning("groq_empty_or_unparseable_response_falling_back_to_local")
        except Exception as exc:
            if not self.allow_fallback:
                raise RuntimeError("Groq generation failed and local fallback is disabled.") from exc
            logger.warning("Groq generation failed. Falling back to local provider.", extra={"error": str(exc)})

        return self._fallback_variants(source_text, content_type, tone, platform, count, brand_terms, directives)

    def _request_variants(self, prompt: str, count: int) -> list[str]:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are NISF's expert marketing copy generator. Return only polished "
                                "user-facing copy variants. Do not include explanations, markdown tables, "
                                "critic notes, internal reasoning, labels, or optimization instructions."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=900,
                )
                content = response.choices[0].message.content or ""
                return self._parse_variants(content, count)
            except Exception as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    raise
                logger.warning(
                    "groq_generation_retry",
                    extra={"attempt": attempt + 1, "max_retries": self.max_retries, "error": str(exc)},
                )
        if last_error is not None:
            raise last_error
        return []

    def generate_critic_feedback(self, text: str, scores: dict[str, float]) -> list[CriticDirectiveSchema]:
        return self.fallback.generate_critic_feedback(text, scores)

    def _build_prompt(
        self,
        source_text: str,
        content_type: str,
        tone: str,
        platform: str,
        count: int,
        brand_terms: list[str] | None,
        directives: list[CriticDirectiveSchema] | None,
    ) -> str:
        terms = ", ".join(brand_terms or []) or "none provided"
        directive_text = " ".join(d.rewrite_instruction for d in directives or []) or "none"
        return (
            f"Generate exactly {count} distinct marketing copy variants.\n\n"
            f"Source and brief:\n{source_text}\n\n"
            f"content_type: {content_type}\n"
            f"tone: {tone}\n"
            f"platform: {platform}\n"
            f"brand_terms: {terms}\n"
            f"private optimization guidance: {directive_text}\n\n"
            "Rules:\n"
            "- Each variant must be clean user-facing copy only.\n"
            "- Respect the selected tone, platform, content_type, and brand terms.\n"
            "- Use correct grammar, natural wording, concrete benefits, and one strong CTA when appropriate.\n"
            "- Prefer specific outcomes over vague claims.\n"
            "- For Instagram, start with a scroll-stopping hook, keep sentences punchy, and avoid corporate wording.\n"
            "- If readability is weak, shorten sentences and remove filler. If engagement is weak, strengthen the hook and CTA.\n"
            f"- Do not use these phrases or close variants of them: {', '.join(self.BANNED_PHRASES)}.\n"
            "- Do not include explanations, markdown tables, headings, numbering, critic notes, or internal reasoning.\n"
            "- Do not include 'Refined focus', 'improve engagement', 'critic feedback', or rewrite instructions.\n"
            "- Return a JSON array of strings only."
        )

    def _parse_variants(self, content: str, count: int) -> list[str]:
        candidates = self._parse_json_array(content) or self._parse_numbered_or_line_list(content)
        variants: list[str] = []
        for candidate in candidates:
            copy = clean_final_copy(candidate)
            if not copy or has_internal_notes(copy) or has_placeholder_text(copy):
                continue
            if copy not in variants:
                variants.append(copy)
            if len(variants) == count:
                break
        return variants

    def _parse_json_array(self, content: str) -> list[str]:
        clean = content.strip()
        match = re.search(r"\[[\s\S]*\]", clean)
        if match:
            clean = match.group(0)
        for parser in (json.loads, ast.literal_eval):
            try:
                parsed = parser(clean)
            except Exception:
                continue
            if isinstance(parsed, list):
                return [str(item) for item in parsed if isinstance(item, str)]
        return []

    def _parse_numbered_or_line_list(self, content: str) -> list[str]:
        lines = []
        for line in content.splitlines():
            cleaned = re.sub(r"^\s*(?:[-*]|\d+[\).:-])\s*", "", line).strip()
            cleaned = cleaned.strip("\"'")
            if cleaned:
                lines.append(cleaned)
        if len(lines) > 1:
            return lines
        sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", content) if part.strip()]
        return sentences

    def _merge_unique(self, current: list[str], incoming: list[str], count: int) -> list[str]:
        merged = list(current)
        seen = {item.lower() for item in merged}
        for candidate in incoming:
            cleaned = clean_final_copy(candidate)
            key = cleaned.lower()
            if not cleaned or key in seen or has_internal_notes(cleaned) or has_placeholder_text(cleaned):
                continue
            merged.append(cleaned)
            seen.add(key)
            if len(merged) == count:
                break
        return merged

    def _fallback_variants(
        self,
        source_text: str,
        content_type: str,
        tone: str,
        platform: str,
        count: int,
        brand_terms: list[str] | None,
        directives: list[CriticDirectiveSchema] | None,
    ) -> list[str]:
        self.last_provider_name = self.fallback.name
        self.last_model_name = self.fallback.model
        return self.fallback.generate_variants(
            source_text=source_text,
            content_type=content_type,
            tone=tone,
            platform=platform,
            count=count,
            brand_terms=brand_terms,
            directives=directives,
        )
