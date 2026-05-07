from app.schemas.critic_schema import CriticDirectiveSchema


class PromptBuilder:
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

    def build_source(self, text: str | None, brief: str | None) -> str:
        if text and brief:
            return f"Source copy: {text}\nCampaign brief: {brief}"
        return text or f"Campaign brief: {brief}"

    def build_generation_prompt(
        self,
        source_text: str,
        content_type: str,
        tone: str,
        platform: str,
        count: int,
        brand_terms: list[str] | None = None,
        directives: list[CriticDirectiveSchema] | None = None,
    ) -> str:
        terms = ", ".join(brand_terms or []) or "none provided"
        directive_text = self.directive_summary(directives) or "none"
        platform_rule = self.platform_guidance(content_type, platform)
        cta_rule = self.cta_guidance(content_type)
        return (
            "Generate marketing text variants as a JSON-compatible list of plain strings.\n"
            f"Source material:\n{source_text}\n\n"
            f"Create exactly {count} distinct variants for content_type={content_type}, "
            f"tone={tone}, platform={platform}.\n"
            "Each variant must use clear, natural language and sound like polished user-facing marketing copy.\n"
            "Each variant must include a distinct hook, specific product benefit, platform-aware wording, strong readability, "
            "and a persuasive emotional angle grounded in real outcomes.\n"
            f"Use these brand terms naturally when relevant: {terms}.\n"
            f"Apply this tone strongly: {self.tone_guidance(tone)}\n"
            f"CTA rule: {cta_rule}\n"
            "Prefer concrete outcomes such as faster multitasking, smoother scrolling, sharper photos, smarter productivity, "
            "AI-assisted daily tasks, better content creation, smoother work and entertainment, reliable performance, or faster everyday actions when relevant.\n"
            "Avoid repeated opening phrases, generic filler, robotic wording, placeholders, weak punctuation, and vague corporate language.\n"
            f"Do not use these phrases or close variants of them: {', '.join(self.BANNED_PHRASES)}.\n"
            f"Platform guidance: {platform_rule}\n"
            f"Use these private optimization directives only to guide the rewrite: {directive_text}\n"
            "Return only clean user-facing variant strings. Do not include markdown, numbering, commentary, "
            "critic notes, labels, explanations, or optimization instructions."
        )

    def directive_summary(self, directives: list[CriticDirectiveSchema] | None) -> str:
        if not directives:
            return ""
        return " ".join(d.rewrite_instruction for d in directives)

    def platform_guidance(self, content_type: str, platform: str) -> str:
        normalized_platform = platform.lower()
        normalized_type = content_type.lower()
        if normalized_type == "ad_copy" and normalized_platform == "instagram":
            return (
                "Start with a daily-life hook that feels Instagram-native, such as 'Your day moves fast. Your phone should too.' "
                "or 'From work mode to weekend shots...'. Mention the product naturally, include 2-3 concrete benefits, "
                "add audience/lifestyle relevance, keep it concise and modern, avoid corporate wording, and end with a direct CTA."
            )
        if normalized_platform in {"instagram", "tiktok", "x"}:
            return "Use concise social copy with a strong first line, fast readability, and a direct action."
        if normalized_platform == "linkedin":
            return "Use professional, credible, benefit-led language that emphasizes productivity, reliability, and clear outcomes without hype."
        if normalized_platform == "email":
            return "Use useful, direct, scannable copy with low-friction language and a clear reason to click."
        if normalized_platform == "google_ads":
            return "Use very concise, benefit-first copy with no fluff."
        return "Use clear web-ready marketing copy with a benefit-led value proposition and a conversion-focused CTA."

    def tone_guidance(self, tone: str) -> str:
        guidance = {
            "professional": "polished, credible, business-focused, and free of hype",
            "friendly": "warm, simple, conversational, and approachable",
            "persuasive": "benefit-led, conversion-focused, and action-oriented",
            "bold": "confident, punchy, high-energy, and direct",
            "luxury": "premium, refined, elegant, and exclusive",
            "playful": "fun, light, energetic, and memorable",
            "urgent": "time-sensitive, action-oriented, and direct",
            "educational": "explanatory, helpful, informative, and practical",
            "clear": "simple, direct, easy to understand, and concise",
        }
        return guidance.get((tone or "clear").lower(), guidance["clear"])

    def cta_guidance(self, content_type: str) -> str:
        normalized = (content_type or "marketing").lower()
        if normalized in {"ad_copy", "social_media", "landing_page_headline", "cta"}:
            return "Include a clear call to action."
        return "Use a CTA only when it improves the user-facing copy naturally."
