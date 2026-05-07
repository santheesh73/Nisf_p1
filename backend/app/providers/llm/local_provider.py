import re

from app.core.config import get_settings
from app.providers.llm.base_llm_provider import BaseLLMProvider
from app.schemas.critic_schema import CriticDirectiveSchema
from app.utils.text_quality import clean_final_copy


class LocalLLMProvider(BaseLLMProvider):
    name = "local"
    model = "nisf-deterministic-local"
    SUPPORTED_TONES = {
        "professional",
        "friendly",
        "persuasive",
        "bold",
        "luxury",
        "playful",
        "urgent",
        "educational",
        "clear",
    }
    TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9'-]*")
    PRODUCT_TERMS = {
        "app",
        "course",
        "courses",
        "device",
        "platform",
        "product",
        "service",
        "serum",
        "solution",
        "smartphone",
        "tool",
        "watch",
        "website",
    }
    STOPWORDS = {
        "a",
        "about",
        "access",
        "all",
        "and",
        "any",
        "are",
        "as",
        "at",
        "be",
        "boost",
        "bring",
        "build",
        "built",
        "by",
        "can",
        "choose",
        "create",
        "daily",
        "designed",
        "discover",
        "do",
        "easy",
        "every",
        "for",
        "from",
        "get",
        "help",
        "helps",
        "in",
        "into",
        "is",
        "it",
        "launch",
        "made",
        "make",
        "more",
        "new",
        "now",
        "of",
        "on",
        "one",
        "our",
        "that",
        "the",
        "their",
        "this",
        "to",
        "today",
        "track",
        "turn",
        "upgrade",
        "use",
        "with",
        "without",
        "you",
        "your",
    }
    TONE_OPENERS = {
        "professional": [
            "Give your workflow a polished way to use {subject} for {features}",
            "{subject} supports {features} in one focused experience",
            "Built for dependable results, {subject} brings {features} to every workflow",
            "Rely on {subject} to manage {features} with confidence",
            "Make {subject} the practical choice for {features}",
        ],
        "friendly": [
            "Meet {subject}, a simple way to enjoy {features}",
            "Make the day easier with {subject} and its support for {features}",
            "{subject} keeps {features} close whenever they matter",
            "Say hello to {subject} for {features} that feel easy to manage",
            "Bring {subject} into the routine and make {features} feel effortless",
        ],
        "persuasive": [
            "Choose {subject} to unlock {features}",
            "Turn everyday needs into real momentum with {subject} and {features}",
            "{subject} gives you a smarter way to get {features}",
            "Make the switch to {subject} for {features} that matter",
            "Get more from every moment with {subject}, built around {features}",
        ],
        "bold": [
            "Move faster with {subject} and take control of {features}",
            "{subject} puts {features} front and center",
            "Stop settling and step up to {subject} for {features}",
            "Bring serious energy to {features} with {subject}",
            "Own the day with {subject}, made for {features}",
        ],
        "luxury": [
            "Experience {subject} with refined support for {features}",
            "{subject} pairs elegant design with {features}",
            "Elevate the everyday with {subject}, crafted around {features}",
            "For a more considered experience, {subject} brings together {features}",
            "{subject} makes {features} feel polished, simple, and premium",
        ],
        "playful": [
            "Give the day a boost with {subject} and {features}",
            "{subject} makes {features} feel a lot more fun",
            "Tap into {subject} for {features} without the usual hassle",
            "Let {subject} handle {features} while the day keeps moving",
            "A better routine starts with {subject}, {features}, and a little more ease",
        ],
        "urgent": [
            "Upgrade now with {subject} and get {features}",
            "Do not wait to make {features} easier with {subject}",
            "Make the switch today to {subject} for {features}",
            "Act now and bring {subject} into the moments that need {features}",
            "Start today with {subject}, built to deliver {features}",
        ],
        "educational": [
            "{subject} helps make {features} easier to understand and manage",
            "With {subject}, {features} become easier to follow and use",
            "Here is the practical value of {subject}: better support for {features}",
            "{subject} brings clear tools for {features} into one experience",
            "Learn how {subject} can simplify {features} for everyday use",
        ],
        "clear": [
            "Stay focused on {features} with {subject}",
            "{subject} helps manage {features} in one place",
            "Use {subject} for {features} without extra hassle",
            "Make every day easier with {subject} and {features}",
            "Get a simpler way to handle {features} with {subject}",
        ],
    }
    STYLE_VARIANTS = ("hook", "benefit", "cta", "emotion", "urgency")
    GENERIC_PHRASES = (
        "revolutionize your daily life",
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
    SMARTPHONE_BENEFITS = [
        "faster multitasking",
        "smoother scrolling",
        "sharper photos",
        "smarter productivity",
        "AI-assisted daily tasks",
        "better content creation",
        "smoother work and entertainment",
        "reliable performance",
        "faster everyday actions",
    ]
    INSTAGRAM_HOOKS = [
        "Your day moves fast. Your phone should too.",
        "Upgrade every scroll, shot, and task.",
        "Busy day? Let your phone keep up.",
        "From first tap to last task, make it smoother.",
        "Work fast. Shoot sharp. Scroll smooth.",
    ]
    TONE_TEMPLATES = {
        "professional": {
            "hook": "{subject_cap} brings a more dependable way to handle busy days.",
            "benefit": "Count on {subject} for {benefit} without adding friction to the day.",
            "cta": "Explore {subject} for reliable performance, practical productivity, and {benefit}.",
            "emotion": "Bring more control and consistency to every day with {subject} and {benefit}.",
            "urgency": "Choose {subject} for a practical upgrade that improves {benefit} today.",
        },
        "friendly": {
            "hook": "Meet {subject}, a smoother way to get through a full day.",
            "benefit": "{subject} makes {benefit} feel easier, quicker, and more natural.",
            "cta": "Try {subject} when you want {benefit} without the extra effort.",
            "emotion": "Bring more ease to work, photos, browsing, and everything between with {subject}.",
            "urgency": "Start today with {subject} and make {benefit} feel simpler.",
        },
        "persuasive": {
            "hook": "Your day moves fast. Discover {subject} built for {benefit}.",
            "benefit": "Upgrade the way you work, create, and stay connected with {subject}, designed for {benefit}.",
            "cta": "Choose {subject} for faster days, sharper moments, and {benefit}.",
            "emotion": "Move through work, content, and everyday tasks with more speed and control thanks to {subject}.",
            "urgency": "Make the switch to {subject} today and feel {benefit} from the first tap.",
        },
        "bold": {
            "hook": "Stop settling for slow. Step up to {subject}.",
            "benefit": "Power every scroll, shot, and task with {subject} built for {benefit}.",
            "cta": "Step up to {subject} and move through the day with {benefit}.",
            "emotion": "Own every moment with {subject} that keeps pace with ambition.",
            "urgency": "Upgrade now to {subject} and feel {benefit} from the first tap.",
        },
        "luxury": {
            "hook": "Experience intelligent performance with a refined edge.",
            "benefit": "{subject_cap} brings {benefit} together in an elegant everyday upgrade.",
            "cta": "Discover {subject} crafted for premium design, effortless productivity, and {benefit}.",
            "emotion": "Elevate each moment with {subject} made for modern ambition.",
            "urgency": "Choose {subject} today for a more considered, premium mobile experience.",
        },
        "playful": {
            "hook": "Make every tap feel a little brighter.",
            "benefit": "{subject_cap} adds energy to {benefit} without making your day complicated.",
            "cta": "Tap into {subject} for smoother work, sharper photos, and more fun on the move.",
            "emotion": "Let {subject} turn daily tasks into quick wins and smarter moments.",
            "urgency": "Jump in today with {subject} and make {benefit} more fun.",
        },
        "urgent": {
            "hook": "Do not wait for a smoother day.",
            "benefit": "Upgrade now to {subject} built for {benefit}.",
            "cta": "Get {subject} today and move faster through work, creation, and connection.",
            "emotion": "When every minute counts, {subject} helps you stay ready.",
            "urgency": "Act today and bring {benefit} into your next task.",
        },
        "educational": {
            "hook": "{subject_cap} can simplify the way you work, create, and connect.",
            "benefit": "With {subject}, {benefit} becomes easier to understand and use every day.",
            "cta": "Learn how {subject} supports smarter workflows, smoother browsing, and practical productivity.",
            "emotion": "A better mobile experience starts with tools that make daily tasks clearer.",
            "urgency": "Explore {subject} today to see how AI can support {benefit}.",
        },
        "clear": {
            "hook": "{subject_cap} helps you do more with less effort.",
            "benefit": "Use {subject} for {benefit} in a simple, reliable way.",
            "cta": "Explore {subject} for smoother work, sharper moments, and easier everyday use.",
            "emotion": "{subject_cap} keeps daily tasks simple, fast, and easy to manage.",
            "urgency": "Start with {subject} today and make {benefit} easier.",
        },
    }

    def __init__(self) -> None:
        self.model = get_settings().local_model

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
        clean = self._clean_source(source_text)
        subject = self._subject(clean, brand_terms)
        features = self._features(clean, subject, brand_terms)
        selected_tone = self._normalize_tone(tone)
        cta = self._cta(platform, selected_tone)
        templates = self.TONE_TEMPLATES[selected_tone]
        context = self._directive_context(directives)
        variants = []
        for index, style in enumerate(self.STYLE_VARIANTS):
            copy = templates[style].format(
                subject=subject,
                subject_cap=self._capitalize_subject(subject),
                benefit=self._benefit_phrase(features[index % len(features)], brand_terms, platform, context),
            )
            copy = self._apply_context(copy, style, subject, brand_terms, platform, content_type, context, index)
            copy = self._adapt_for_content_type(copy, content_type, index)
            copy = self._adapt_for_platform(copy, platform, selected_tone)
            copy = self._add_cta(copy, content_type, platform, selected_tone, cta, index)
            variants.append(self._polish(copy, content_type, platform))
        return self._dedupe(variants)[:count]

    def generate_critic_feedback(self, text: str, scores: dict[str, float]) -> list[CriticDirectiveSchema]:
        weakest = sorted((k, v) for k, v in scores.items() if k != "attention_coefficient")[:3]
        directives: list[CriticDirectiveSchema] = []
        for priority, (dimension, score) in enumerate(sorted(scores.items(), key=lambda item: item[1])[:3], start=1):
            if dimension == "attention_coefficient":
                continue
            directives.append(
                CriticDirectiveSchema(
                    target_dimension=dimension,
                    issue=f"{dimension.replace('_', ' ').title()} is below target at {score:.1f}.",
                    rewrite_instruction=self._rewrite_instruction(dimension),
                    priority=priority,
                    risk_level="medium" if score < 55 else "low",
                )
            )
        return directives or [
            CriticDirectiveSchema(
                target_dimension="engagement",
                issue="The content could invite a stronger action.",
                rewrite_instruction="Add a concrete benefit and direct call to action.",
                priority=1,
                risk_level="low",
            )
        ]

    def _clean_source(self, source_text: str) -> str:
        if "Source material:" in source_text:
            source_text = source_text.split("Source material:", 1)[1].split("Create exactly", 1)[0]
        clean = " ".join(source_text.replace("Source copy:", "").replace("Campaign brief:", "").split())
        return clean.rstrip(".") or "your product"

    def _directive_context(self, directives: list[CriticDirectiveSchema] | None) -> dict[str, bool]:
        targets = {(directive.target_dimension or "").lower() for directive in directives or []}
        return {
            "readability": "readability" in targets,
            "engagement": "engagement" in targets,
            "brand_fit": "brand_fit" in targets,
            "clarity": "clarity" in targets,
            "emotional_resonance": "emotional_resonance" in targets,
        }

    def _brand_phrase(self, brand_terms: list[str] | None) -> str:
        terms = [term.strip() for term in brand_terms or [] if term.strip()]
        if not terms:
            return ""
        lowered = {term.lower() for term in terms}
        if {"ai-powered", "smartphone"}.issubset(lowered):
            return "an AI-powered smartphone"
        if len(terms) == 1:
            return terms[0]
        return ", ".join(terms[:-1]) + f", and {terms[-1]}"

    def _subject(self, source_text: str, brand_terms: list[str] | None) -> str:
        brand_subject = self._brand_subject(brand_terms)
        if brand_subject:
            return brand_subject

        phrases = self._phrases(source_text)
        for phrase in phrases:
            if any(term in phrase.lower().split() for term in self.PRODUCT_TERMS):
                return phrase
        return phrases[0] if phrases else self._fallback_subject(source_text)

    def _features(self, source_text: str, subject: str, brand_terms: list[str] | None) -> list[str]:
        phrases = self._phrases(source_text)
        subject_words = set(self._tokens(subject))
        feature_parts: list[str] = []

        for term in brand_terms or []:
            words = set(self._tokens(term))
            if words and not words.issubset(subject_words):
                self._append_unique(feature_parts, term)

        for phrase in phrases:
            words = set(self._tokens(phrase))
            if not words or words.issubset(subject_words):
                continue
            self._append_unique(feature_parts, phrase)

        for token in self._tokens(source_text):
            if token in subject_words or token in self.STOPWORDS:
                continue
            self._append_unique(feature_parts, token)

        if not feature_parts:
            feature_parts = [subject]

        feature_groups = [
            self._join_terms(feature_parts[:3]),
            self._join_terms(feature_parts[1:4] or feature_parts[:3]),
            self._join_terms(feature_parts[2:5] or feature_parts[:3]),
            self._join_terms((feature_parts[:1] + feature_parts[3:5]) or feature_parts[:3]),
            self._join_terms(feature_parts[:2] + feature_parts[-1:]),
        ]
        return [group for group in feature_groups if group]

    def _brand_subject(self, brand_terms: list[str] | None) -> str:
        terms = [term.strip() for term in brand_terms or [] if term.strip()]
        if not terms:
            return ""
        lowered = {term.lower() for term in terms}
        if {"ai-powered", "smartphone"}.issubset(lowered):
            return "an AI-powered smartphone"
        for index, term in enumerate(terms):
            term_words = set(self._tokens(term))
            if not term_words.intersection(self.PRODUCT_TERMS):
                continue
            previous = terms[index - 1] if index > 0 else ""
            previous_words = self._tokens(previous)
            if previous and len(previous_words) <= 2 and not set(previous_words).intersection(self.PRODUCT_TERMS):
                return f"{previous} {term}"
            return term
        return self._brand_phrase(terms)

    def _phrases(self, source_text: str) -> list[str]:
        phrases: list[str] = []
        for segment in re.split(r"[,.;:!?()]+|\s+-\s+", source_text):
            words = self.TOKEN_PATTERN.findall(segment)
            current: list[str] = []
            for word in words:
                normalized = word.lower().strip("-'")
                if normalized in self.STOPWORDS:
                    self._flush_phrase(current, phrases)
                    current = []
                    continue
                current.append(word)
            self._flush_phrase(current, phrases)

        cleaned: list[str] = []
        for phrase in phrases:
            tokens = phrase.split()
            if len(tokens) > 4:
                tokens = tokens[:4]
            self._append_unique(cleaned, " ".join(tokens))
        return cleaned

    def _flush_phrase(self, current: list[str], phrases: list[str]) -> None:
        if not current:
            return
        phrase = " ".join(current).strip(" ,-")
        if len(phrase) >= 3:
            self._append_unique(phrases, phrase)

    def _tokens(self, text: str) -> list[str]:
        return [token.lower().strip("-'") for token in self.TOKEN_PATTERN.findall(text)]

    def _fallback_subject(self, source_text: str) -> str:
        words = [word for word in source_text.split() if word.lower().strip(".,!?") not in self.STOPWORDS]
        return " ".join(words[:4]).strip(" .,!?") or "your offer"

    def _join_terms(self, terms: list[str]) -> str:
        clean_terms = [term for term in terms if term]
        if not clean_terms:
            return ""
        if len(clean_terms) == 1:
            return clean_terms[0]
        if len(clean_terms) == 2:
            return f"{clean_terms[0]} and {clean_terms[1]}"
        return ", ".join(clean_terms[:-1]) + f", and {clean_terms[-1]}"

    def _append_unique(self, values: list[str], value: str) -> None:
        normalized = " ".join(value.split()).strip(" .,-")
        if not normalized:
            return
        lowered = normalized.lower()
        existing_values = [item.lower() for item in values]
        if any(lowered == item or lowered in item or item in lowered for item in existing_values):
            return
        values.append(normalized)

    def _content_type_tail(self, content_type: str, index: int) -> str:
        normalized = content_type.lower()
        if normalized == "email":
            return " with a clear reason to click"
        if normalized in {"ad", "ad_copy", "headline", "marketing", "tagline"}:
            return ""
        return ""

    def _dedupe(self, variants: list[str]) -> list[str]:
        unique: list[str] = []
        seen: set[str] = set()
        for variant in variants:
            key = variant.lower()
            if key not in seen:
                unique.append(variant)
                seen.add(key)
        return unique

    def _normalize_tone(self, tone: str) -> str:
        normalized = (tone or "clear").strip().lower()
        if normalized in self.SUPPORTED_TONES:
            return normalized
        if normalized in {"confident", "energetic"}:
            return "bold"
        if normalized in {"premium", "elegant"}:
            return "luxury"
        return "clear"

    def _cta(self, platform: str, tone: str) -> str:
        platform = platform.lower()
        if tone == "urgent":
            return "Upgrade now"
        if tone == "luxury":
            return "Experience it today"
        if tone == "educational":
            return "Learn more today"
        if tone == "professional":
            return "Explore the upgrade"
        if tone == "playful":
            return "Tap in today"
        if platform == "instagram":
            return "Tap to explore today"
        if platform == "linkedin":
            return "See how it can work for your team"
        if platform == "email":
            return "Explore the offer now"
        return "Discover the smarter way today"

    def _directive_tail(self, directives: list[CriticDirectiveSchema] | None) -> str:
        if not directives:
            return ""
        focus = directives[0].rewrite_instruction.rstrip(".")
        return ""

    def _polish(self, text: str, content_type: str, platform: str) -> str:
        clean = clean_final_copy(" ".join(text.split()))
        clean = self._replace_generic_phrases(clean)
        clean = clean.replace(" .", ".").replace("..", ".")
        if content_type.lower() == "ad_copy" and platform.lower() == "instagram":
            sentences = [sentence.strip() for sentence in clean.split(".") if sentence.strip()]
            clean = ". ".join(sentences[:3])
            if clean and not clean.endswith("."):
                clean += "."
        return clean

    def _rewrite_instruction(self, dimension: str) -> str:
        instructions = {
            "engagement": "Strengthen the opening hook, make the first benefit more immediate, and end with a clearer CTA.",
            "clarity": "State the product and benefit more directly with concrete wording.",
            "emotional_resonance": "Connect the copy to speed, confidence, creativity, ease, or control without exaggeration.",
            "brand_fit": "Use the brand terms naturally and make them feel integral to the message.",
            "readability": "Shorten sentences, simplify word choice, and remove corporate filler.",
            "originality": "Use more distinctive wording, avoid generic claims, and prefer specific outcomes.",
            "safety": "Remove risky wording and keep the copy appropriate.",
        }
        return instructions.get(dimension, "Improve the weakest quality dimension while keeping the copy user-facing.")

    def _capitalize_subject(self, subject: str) -> str:
        return subject[:1].upper() + subject[1:] if subject else subject

    def _benefit_phrase(self, feature: str, brand_terms: list[str] | None, platform: str, context: dict[str, bool]) -> str:
        lowered_terms = {term.lower() for term in brand_terms or []}
        if {"ai-powered", "smartphone", "mobile experience"}.issubset(lowered_terms):
            if platform.lower() == "instagram":
                return "smoother work, sharper photos, and faster everyday tasks"
            return "smoother work, sharper moments, and faster everyday actions"
        if not feature:
            return "clearer results and easier everyday use"
        if "smoother work, sharper moments" in feature:
            return feature
        if context.get("readability"):
            return self._shorten_benefit(feature)
        return feature

    def _shorten_benefit(self, feature: str) -> str:
        compact = feature.replace(" and ", ", ")
        words = compact.split()
        if len(words) <= 6:
            return compact
        return " ".join(words[:6]).rstrip(",")

    def _apply_context(
        self,
        copy: str,
        style: str,
        subject: str,
        brand_terms: list[str] | None,
        platform: str,
        content_type: str,
        context: dict[str, bool],
        index: int,
    ) -> str:
        normalized_platform = (platform or "web").lower()
        normalized_type = (content_type or "marketing").lower()
        result = copy

        if normalized_platform == "instagram" and normalized_type in {"ad_copy", "social_media"} and style == "hook":
            result = self.INSTAGRAM_HOOKS[index % len(self.INSTAGRAM_HOOKS)]

        if context.get("clarity"):
            result = self._make_more_direct(result, subject)
        if context.get("engagement"):
            result = self._boost_engagement(result, normalized_platform, style, index)
        if context.get("emotional_resonance"):
            result = self._add_emotional_pull(result)
        if context.get("brand_fit"):
            result = self._add_brand_term_naturally(result, brand_terms)
        if context.get("readability"):
            result = self._simplify(result)

        return result

    def _make_more_direct(self, text: str, subject: str) -> str:
        direct = text.replace("brings a more dependable way to handle busy days", f"is built for busy days with {subject}")
        return direct.replace("Upgrade the way you work, create, and stay connected", "Work faster, create sharper, and get more done")

    def _boost_engagement(self, text: str, platform: str, style: str, index: int) -> str:
        if platform == "instagram" and style in {"hook", "benefit"}:
            return [
                "Your day moves fast. Your phone should too.",
                "Upgrade every scroll, shot, and task.",
                "Work fast. Shoot sharp. Stay in flow.",
                "Busy day? This upgrade keeps up.",
                "Do more between your first tap and last task.",
            ][index % 5]
        return text

    def _add_emotional_pull(self, text: str) -> str:
        if any(word in text.lower() for word in ("confidence", "control", "ease", "creative", "focus")):
            return text
        return f"{text.rstrip('.')} and feel more in control through every part of the day."

    def _add_brand_term_naturally(self, text: str, brand_terms: list[str] | None) -> str:
        terms = [term.strip() for term in brand_terms or [] if term.strip()]
        if not terms:
            return text
        if any(term.lower() in text.lower() for term in terms):
            return text
        return f"{text.rstrip('.')} Built around {terms[0]}."

    def _simplify(self, text: str) -> str:
        simplified = text.replace("designed for", "built for")
        simplified = simplified.replace("discover", "see")
        sentences = [sentence.strip() for sentence in simplified.split(".") if sentence.strip()]
        compact = []
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 14:
                compact.append(" ".join(words[:14]).rstrip(","))
            else:
                compact.append(sentence)
        return ". ".join(compact) + ("." if compact else "")

    def _replace_generic_phrases(self, text: str) -> str:
        clean = text
        replacements = {
            "revolutionize your daily life": "make everyday tasks faster and easier",
            "unlock your potential": "get more done every day",
            "take it to the next level": "upgrade the way you work and create",
            "cutting-edge": "advanced",
            "game-changing": "worth the upgrade",
            "innovative solution": "practical upgrade",
            "smarter way to interact": "faster everyday use",
            "create and innovate": "create with less friction",
            "seamless experience": "smooth experience",
            "empower your journey": "help you stay in control",
            "transform your world": "improve your everyday routine",
        }
        for phrase, replacement in replacements.items():
            clean = re.sub(re.escape(phrase), replacement, clean, flags=re.IGNORECASE)
        return clean

    def _adapt_for_content_type(self, copy: str, content_type: str, index: int) -> str:
        normalized = (content_type or "marketing").lower()
        if normalized == "email":
            return f"Subject: A smarter upgrade for your day. {copy}"
        if normalized == "product_description":
            return f"{copy} It pairs practical features with clear everyday benefits."
        if normalized == "blog_intro":
            return f"Modern routines ask more from every device. {copy}"
        if normalized == "landing_page_headline":
            return self._shorten(copy, 14)
        if normalized == "cta":
            return ["Discover the upgrade", "Explore it today", "Make the switch", "Start smarter", "Upgrade now"][
                index % 5
            ]
        if normalized == "microcopy":
            return ["Continue with confidence", "Your upgrade is ready", "See the smarter option", "Tap to explore", "Start here"][
                index % 5
            ]
        if normalized == "social_media":
            return copy.replace(". ", ".\n")
        return copy

    def _adapt_for_platform(self, copy: str, platform: str, tone: str) -> str:
        normalized = (platform or "web").lower()
        if normalized == "instagram":
            return copy
        if normalized == "linkedin":
            return copy.replace("Your day", "Modern work").replace("every tap", "every workflow")
        if normalized == "google_ads":
            return self._shorten(copy, 18)
        if normalized == "youtube":
            return f"Ready for the upgrade? {copy}"
        if normalized in {"x_twitter", "x", "twitter"}:
            return self._shorten(copy, 20)
        if normalized == "email" and tone != "playful":
            return copy.replace("Tap", "Click")
        return copy

    def _add_cta(self, copy: str, content_type: str, platform: str, tone: str, cta: str, index: int) -> str:
        normalized_type = (content_type or "marketing").lower()
        if normalized_type in {"product_description", "blog_intro", "landing_page_headline", "microcopy", "cta"}:
            return copy
        if copy.rstrip().endswith((".", "!", "?")):
            return f"{copy} {cta}."
        return f"{copy}. {cta}."

    def _shorten(self, copy: str, max_words: int) -> str:
        words = copy.split()
        if len(words) <= max_words:
            return copy
        return " ".join(words[:max_words]).rstrip(" ,;:")
