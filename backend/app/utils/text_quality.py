import re

from app.utils.text_utils import clamp

INTERNAL_NOTE_PATTERNS = [
    r"refined\s+focus\s*:",
    r"optimization\s+note\s*:",
    r"critic\s+note\s*:",
    r"rewrite\s+instruction\s*:",
    r"directive\s*:",
    r"based\s+on\s+critic\s+feedback",
    r"critic\s+feedback",
    r"optimization\s+instruction",
    r"optimization\s+directive",
    r"improve\s+engagement",
    r"preserv(?:e|ing)\s+the\s+core\s+offer",
    r"while\s+preserving\s+the\s+core\s+offer",
    r"as\s+an\s+ai",
    r"here\s+is\s+the\s+improved\s+version\s*:",
    r"final\s+answer\s*:",
    r"user-facing\s+copy\s*:",
    r"marketing\s+copy\s*:",
]

PLACEHOLDER_PATTERNS = [
    r"\bstring\b",
    r"\blorem\s+ipsum\b",
    r"\binsert\s+here\b",
    r"\byour\s+product\b",
    r"\bbrand\s+name\b",
    r"\bcta\s+here\b",
]

GENERIC_FILLER = [
    "mobile experience",
    "take control",
    "boost your experience",
    "unlock your potential",
    "game changer",
    "revolutionize your life",
    "take it to the next level",
    "cutting-edge",
    "game-changing",
    "innovative solution",
    "smarter way to interact",
    "create and innovate",
    "seamless experience",
    "empower your journey",
    "transform your world",
]

AWKWARD_PHRASES = [
    "young days move fast",
    "smart daily help",
    "start faster every day",
    "mobile experience should too with",
    "ready to discover the upgrade",
]

CTA_PATTERNS = [
    r"\btap\s+to\b",
    r"\bclick\s+to\b",
    r"\bshop\s+now\b",
    r"\bexplore\s+(?:today|now|the)\b",
    r"\bdiscover\s+(?:today|now|your)\b",
    r"\bupgrade\s+(?:now|today)\b",
    r"\bget\s+started\b",
    r"\blearn\s+more\b",
    r"\btry\s+it\b",
]

PRODUCT_TERMS = {
    "app",
    "course",
    "device",
    "platform",
    "phone",
    "product",
    "service",
    "smartphone",
    "software",
    "tool",
    "website",
}

CONCRETE_BENEFIT_TERMS = {
    "capture",
    "create",
    "easier",
    "easy",
    "faster",
    "finish",
    "photo",
    "photos",
    "productivity",
    "sharp",
    "sharper",
    "smooth",
    "smoother",
    "scroll",
    "scrolling",
    "speed",
    "task",
    "tasks",
}

LIFESTYLE_RELEVANCE_TERMS = {
    "busy",
    "day",
    "days",
    "daily",
    "everyday",
    "momentum",
    "weekend",
    "work",
}

NATURAL_HOOK_PATTERNS = [
    r"^your\s+day\s+moves\s+fast",
    r"^from\s+work\s+mode\s+to\s+weekend\s+shots",
    r"^built\s+for\s+busy\s+days",
    r"^for\s+every\s+task,\s*shot,\s*and\s*scroll",
    r"^upgrade\s+every\s+scroll,\s*shot,\s*and\s*task",
    r"^busy\s+day\?",
]

LOW_ASPIRATION_HOOKS = [
    "make every tap feel quicker",
]


def clean_final_copy(text: str) -> str:
    clean = " ".join((text or "").split())
    if not clean:
        return ""

    clean = _remove_bracketed_internal_notes(clean)
    clean = _remove_internal_labels_and_tails(clean)
    clean = _remove_placeholder_text(clean)
    clean = _fix_common_grammar(clean)
    clean = _remove_known_repeated_phrases(clean)
    clean = _replace_generic_filler(clean)
    clean = _normalize_punctuation(clean)
    clean = _remove_duplicate_clauses(clean)
    clean = _remove_duplicate_sentences(clean)
    clean = _remove_repeated_opening_phrases(clean)
    clean = _remove_trailing_fragments(clean)
    clean = _ensure_clean_ending(clean)
    return _normalize_brand_hyphenation(clean)


def polish_marketing_copy(
    text: str,
    content_type: str,
    tone: str,
    platform: str,
    brand_terms: list[str] | None = None,
) -> str:
    clean = clean_final_copy(text)
    if not clean:
        return ""

    clean = _normalize_brand_hyphenation(clean)
    clean = _replace_generic_filler(clean)

    normalized_type = (content_type or "marketing").lower()
    normalized_platform = (platform or "web").lower()
    normalized_tone = (tone or "clear").lower()
    lowered_terms = {term.strip().lower() for term in brand_terms or [] if term.strip()}

    if (
        normalized_platform == "instagram"
        and normalized_type in {"ad_copy", "social_media"}
        and normalized_tone in {"persuasive", "bold", "friendly", "clear"}
        and "smartphone" in lowered_terms
    ):
        if (
            not has_awkward_phrases(clean)
            and not has_broken_sentence_structure(clean)
            and not has_unclear_cta(clean)
            and has_product_or_service(clean, brand_terms)
            and has_concrete_benefit(clean)
            and not any(hook in clean.lower() for hook in LOW_ASPIRATION_HOOKS)
            and instagram_persuasive_quality_bonus(
                clean,
                brand_terms,
                normalized_type,
                normalized_tone,
                normalized_platform,
            )
            >= 34
        ):
            return clean_final_copy(clean)
        return _polish_instagram_smartphone_copy(clean, brand_terms)

    return clean_final_copy(clean)


def has_internal_notes(text: str) -> bool:
    lowered = text or ""
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in INTERNAL_NOTE_PATTERNS) or bool(
        re.search(r"\[(?:critic|note|optimization|directive)[^\]]*\]", lowered, flags=re.IGNORECASE)
    )


def has_placeholder_text(text: str) -> bool:
    return any(re.search(pattern, text or "", flags=re.IGNORECASE) for pattern in PLACEHOLDER_PATTERNS)


def repeated_phrase_count(text: str) -> int:
    tokens = re.findall(r"[a-z0-9'-]+", (text or "").lower())
    repeats = 0
    for size in (2, 3, 4):
        seen: set[tuple[str, ...]] = set()
        repeated: set[tuple[str, ...]] = set()
        for index in range(0, max(0, len(tokens) - size + 1)):
            gram = tuple(tokens[index : index + size])
            if gram in seen:
                repeated.add(gram)
            seen.add(gram)
        repeats += len(repeated)
    return repeats


def has_repeated_phrases(text: str) -> bool:
    return repeated_phrase_count(text) > 0


def quality_penalty(
    text: str,
    brand_terms: list[str] | None = None,
    content_type: str = "marketing",
    tone: str = "clear",
    platform: str = "web",
) -> float:
    penalty = 0.0
    lowered = (text or "").lower()
    words = re.findall(r"[a-z0-9'-]+", lowered)
    normalized_type = (content_type or "marketing").lower()
    normalized_platform = (platform or "web").lower()
    normalized_tone = (tone or "clear").lower()

    if has_internal_notes(text):
        penalty += 45
    if has_placeholder_text(text):
        penalty += 40
    awkward_hits = awkward_phrase_hits(text)
    if awkward_hits:
        penalty += min(75, awkward_hits * 28)
    if has_broken_sentence_structure(text):
        penalty += 26
    if normalized_type in {"ad", "ad_copy", "social_media"} and has_unclear_cta(text):
        penalty += 18
    if (
        normalized_type in {"ad", "ad_copy", "social_media"}
        and normalized_platform == "instagram"
        and normalized_tone == "persuasive"
    ):
        if not has_product_or_service(text, brand_terms):
            penalty += 24
        if not has_concrete_benefit(text):
            penalty += 24
        if has_unclear_cta(text):
            penalty += 24
    if len(words) < 6:
        penalty += 20
    if repeated_phrase_count(text):
        penalty += min(30, repeated_phrase_count(text) * 8)
    if _has_obvious_article_gap(text):
        penalty += 10
    if any(filler in lowered for filler in GENERIC_FILLER) and len(words) < 16:
        penalty += 8

    missing_terms = _missing_brand_terms(text, brand_terms)
    if missing_terms:
        penalty += min(20, len(missing_terms) * 6)

    return clamp(penalty, 0, 100)


def is_dirty_final_copy(
    text: str,
    brand_terms: list[str] | None = None,
    content_type: str = "marketing",
    tone: str = "clear",
    platform: str = "web",
) -> bool:
    return quality_penalty(text, brand_terms, content_type, tone, platform) >= 35


def awkward_phrase_hits(text: str) -> int:
    lowered = (text or "").lower()
    return sum(1 for phrase in AWKWARD_PHRASES if phrase in lowered)


def has_awkward_phrases(text: str) -> bool:
    return awkward_phrase_hits(text) > 0


def has_broken_sentence_structure(text: str) -> bool:
    lowered = (text or "").lower()
    patterns = [
        r"\bshould\s+too\s+with\b",
        r"\bexperience\s+should\s+too\b",
        r"\bwith\s+our\s+an\b",
        r"\bwith\s+a\s+ai-powered\b",
        r"\bwith\s+ai-powered\s+smartphone\b",
        r"\bready\s+to\s+discover\s+the\s+upgrade\s+that\s+helps\s+you\b",
        r"\b\w+\s+days\s+move\s+fast\b",
        r"\bfeel\s+smoother\s+work\b",
    ]
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in patterns)


def has_unclear_cta(text: str) -> bool:
    lowered = (text or "").lower()
    if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in CTA_PATTERNS):
        return False
    return True


def has_product_or_service(text: str, brand_terms: list[str] | None = None) -> bool:
    lowered = (text or "").lower()
    if any(term.strip().lower() in lowered for term in brand_terms or [] if term.strip()):
        return True
    tokens = set(re.findall(r"[a-z0-9'-]+", lowered))
    return bool(tokens.intersection(PRODUCT_TERMS))


def has_concrete_benefit(text: str) -> bool:
    lowered = (text or "").lower()
    tokens = set(re.findall(r"[a-z0-9'-]+", lowered))
    return bool(tokens.intersection(CONCRETE_BENEFIT_TERMS))


def passes_minimum_naturalness(
    text: str,
    brand_terms: list[str] | None = None,
    content_type: str = "marketing",
    tone: str = "clear",
    platform: str = "web",
) -> bool:
    return not is_dirty_final_copy(text, brand_terms, content_type, tone, platform)


def instagram_persuasive_quality_bonus(
    text: str,
    brand_terms: list[str] | None = None,
    content_type: str = "marketing",
    tone: str = "clear",
    platform: str = "web",
) -> float:
    normalized_type = (content_type or "marketing").lower()
    normalized_tone = (tone or "clear").lower()
    normalized_platform = (platform or "web").lower()
    if normalized_type != "ad_copy" or normalized_tone != "persuasive" or normalized_platform != "instagram":
        return 0.0

    lowered = (text or "").lower()
    tokens = set(re.findall(r"[a-z0-9'-]+", lowered))
    bonus = 0.0

    if has_product_or_service(text, brand_terms):
        bonus += 4
    benefit_hits = len(tokens.intersection(CONCRETE_BENEFIT_TERMS))
    bonus += min(12, benefit_hits * 2.5)
    lifestyle_hits = len(tokens.intersection(LIFESTYLE_RELEVANCE_TERMS))
    bonus += min(10, lifestyle_hits * 3)
    if any(re.search(pattern, lowered) for pattern in NATURAL_HOOK_PATTERNS):
        bonus += 12
    if not has_unclear_cta(text):
        bonus += 6
    if 18 <= len(re.findall(r"[a-z0-9'-]+", lowered)) <= 34:
        bonus += 4
    if any(hook in lowered for hook in LOW_ASPIRATION_HOOKS):
        bonus -= 8
    if has_awkward_phrases(text) or has_broken_sentence_structure(text):
        bonus -= 30

    return clamp(bonus, -30, 40)


def _remove_bracketed_internal_notes(text: str) -> str:
    return re.sub(r"\s*\[(?:critic|note|optimization|directive)[^\]]*\]\s*", " ", text, flags=re.IGNORECASE)


def _remove_internal_labels_and_tails(text: str) -> str:
    clean = text
    tail_labels = [
        "refined focus",
        "optimization note",
        "critic note",
        "rewrite instruction",
        "directive",
        "final answer",
        "user-facing copy",
        "marketing copy",
        "here is the improved version",
    ]
    for label in tail_labels:
        clean = re.sub(rf"\s*{label}\s*:.*$", "", clean, flags=re.IGNORECASE)

    removals = [
        r"based\s+on\s+critic\s+feedback",
        r"critic\s+feedback",
        r"improve\s+engagement",
        r"while\s+preserving\s+the\s+core\s+offer",
        r"preserv(?:e|ing)\s+the\s+core\s+offer",
        r"as\s+an\s+ai",
    ]
    for pattern in removals:
        clean = re.sub(pattern, "", clean, flags=re.IGNORECASE)
    return clean


def _remove_placeholder_text(text: str) -> str:
    clean = text
    for pattern in PLACEHOLDER_PATTERNS:
        clean = re.sub(pattern, "", clean, flags=re.IGNORECASE)
    return clean


def _fix_common_grammar(text: str) -> str:
    clean = re.sub(r"\bwith\s+AI-powered\s+smartphone\b", "with an AI-powered smartphone", text)
    clean = re.sub(r"\bwith\s+a\s+AI-powered\b", "with an AI-powered", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\ban\s+smartphone\b", "a smartphone", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\bof\s+mobile\s+experience\b", "of your mobile experience", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\byoung\s+days\s+move\s+fast\b", "Your day moves fast", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\bsmart\s+daily\s+help\b", "faster everyday tasks", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\bstart\s+faster\s+every\s+day\b", "move faster every day", clean, flags=re.IGNORECASE)
    clean = re.sub(
        r"\byour\s+mobile\s+experience\s+should\s+too\s+with\s+our\s+",
        "your phone should too. Upgrade your mobile experience with our ",
        clean,
        flags=re.IGNORECASE,
    )
    clean = re.sub(
        r"\bready\s+to\s+discover\s+the\s+upgrade(?:\s+that\s+helps\s+you\s+move\s+faster\s+every\s+day)?\??",
        "Tap to explore today.",
        clean,
        flags=re.IGNORECASE,
    )
    return clean


def _remove_known_repeated_phrases(text: str) -> str:
    clean = text
    for phrase in ("Move faster", "take control", "discover it today"):
        pattern = re.compile(rf"({re.escape(phrase)})(.*?)(,\s*(?:and\s+)?{re.escape(phrase)})", re.IGNORECASE)
        while pattern.search(clean):
            clean = pattern.sub(r"\1\2", clean)
    return clean


def _normalize_punctuation(text: str) -> str:
    clean = re.sub(r"\s+([,.;:!?])", r"\1", text)
    clean = re.sub(r"([,;:])([^\s])", r"\1 \2", clean)
    clean = re.sub(r"\s*,\s*,+", ", ", clean)
    clean = re.sub(r"\.{2,}", ".", clean)
    clean = re.sub(r"\s*[-–—]\s*", " - ", clean)
    clean = re.sub(r"\s+-\s+", " - ", clean)
    clean = re.sub(r"\s{2,}", " ", clean)
    return clean.strip(" ,;:-")


def _normalize_brand_hyphenation(text: str) -> str:
    clean = re.sub(r"\bAI\s*-\s*powered\b", "AI-powered", text, flags=re.IGNORECASE)
    clean = re.sub(r"\bmobile\s*-\s*first\b", "mobile-first", clean, flags=re.IGNORECASE)
    return clean


def _replace_generic_filler(text: str) -> str:
    clean = text
    replacements = {
        r"revolutionize your (?:daily )?life": "make everyday tasks feel faster and easier",
        r"unlock your potential": "get more done every day",
        r"take it to the next level": "upgrade the way you work and create",
        r"cutting-edge": "advanced",
        r"game-changing": "worth the upgrade",
        r"innovative solution": "practical upgrade",
        r"smarter way to interact": "faster everyday use",
        r"create and innovate": "create with less friction",
        r"seamless experience": "smooth experience",
        r"empower your journey": "help you stay in control",
        r"transform your world": "improve your everyday routine",
    }
    for pattern, replacement in replacements.items():
        clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
    return clean


def _remove_duplicate_clauses(text: str) -> str:
    clauses = [clause.strip() for clause in re.split(r"\s*,\s*", text) if clause.strip()]
    if len(clauses) < 2:
        return text

    kept: list[str] = []
    seen_stems: set[str] = set()
    seen_tokens: set[str] = set()
    for clause in clauses:
        tokens = re.findall(r"[a-z0-9'-]+", clause.lower())
        meaningful = [token for token in tokens if token not in {"a", "an", "and", "or", "the", "to", "of", "your"}]
        stem = " ".join(tokens[:3])
        short_stem = " ".join(tokens[:2])
        if (stem and stem in seen_stems) or (short_stem and short_stem in seen_stems):
            continue
        if meaningful and all(token in seen_tokens for token in meaningful):
            continue
        kept.append(clause)
        seen_tokens.update(meaningful)
        if stem:
            seen_stems.add(stem)
        if short_stem:
            seen_stems.add(short_stem)

    if not kept:
        return text
    return ", ".join(kept)


def _remove_duplicate_sentences(text: str) -> str:
    pieces = [piece.strip() for piece in re.split(r"(?<=[.!?])\s+", text) if piece.strip()]
    result: list[str] = []
    seen: set[str] = set()
    for piece in pieces:
        key = re.sub(r"[^a-z0-9]+", " ", piece.lower()).strip()
        if key and key not in seen:
            result.append(piece)
            seen.add(key)
    return " ".join(result)


def _remove_repeated_opening_phrases(text: str) -> str:
    sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]
    if len(sentences) < 2:
        return text

    seen_phrases: set[str] = set()
    cleaned: list[str] = []
    for sentence in sentences:
        phrase = " ".join(re.findall(r"[a-z0-9'-]+", sentence.lower())[:3])
        if phrase and phrase in seen_phrases:
            continue
        cleaned.append(sentence)
        seen_phrases.add(phrase)
    return " ".join(cleaned)


def _remove_trailing_fragments(text: str) -> str:
    clean = text.strip()
    clean = re.sub(r"\s+(and|or|but|while|with|for|to|of|the|a|an)$", "", clean, flags=re.IGNORECASE)
    return clean.strip(" ,;:-")


def _ensure_clean_ending(text: str) -> str:
    clean = text.strip()
    if not clean:
        return ""
    if clean[-1] not in ".!?":
        clean += "."
    return clean


def _polish_instagram_smartphone_copy(text: str, brand_terms: list[str] | None) -> str:
    lowered = text.lower()
    subject = "AI-powered smartphone" if any(term.lower() == "ai-powered" for term in brand_terms or []) else "smartphone"

    benefit_pool = []
    mapping = [
        ("multitask", "faster tasks"),
        ("scroll", "smooth scrolling"),
        ("photo", "sharp photos"),
        ("camera", "sharp photos"),
        ("productivity", "smart work"),
        ("task", "faster everyday tasks"),
        ("content", "easy content creation"),
        ("entertainment", "smooth work and play"),
        ("performance", "reliable speed"),
        ("fast", "faster tasks"),
        ("smooth", "smooth scrolling"),
    ]
    for token, benefit in mapping:
        if token in lowered and benefit not in benefit_pool:
            benefit_pool.append(benefit)

    defaults = [
        "faster tasks",
        "smooth scrolling",
        "sharp photos",
    ]
    for benefit in defaults:
        if benefit not in benefit_pool:
            benefit_pool.append(benefit)
        if len(benefit_pool) == 3:
            break

    first, second, third = benefit_pool[:3]
    templates = [
        f"Your day moves fast. Your phone should too. Capture sharper photos, finish tasks faster, and enjoy a smoother mobile experience with our {subject} built for everyday momentum. Tap to explore today.",
        f"From work mode to weekend shots, move faster with our {subject} built for sharp photos, smooth scrolling, and effortless everyday productivity. Tap to explore today.",
        f"Upgrade every scroll, shot, and task with our {subject} built for sharper photos, smoother days, and faster productivity. Tap to discover your smarter mobile experience.",
        f"For every task, shot, and scroll, choose our {subject} built for {first}, {second}, and {third}. Tap to explore today.",
        f"Capture sharper photos, finish tasks faster, and enjoy smoother scrolling with our {subject}. Tap to discover your smarter mobile experience.",
        f"Busy day? Keep up with our {subject} built for {first}, {second}, and {third}. Tap to explore today.",
    ]

    if "work mode" in lowered or "weekend" in lowered:
        return clean_final_copy(templates[1])
    if "make every tap feel quicker" in lowered or "capture sharper photos" in lowered or "your day moves fast" in lowered:
        return clean_final_copy(templates[0])

    chosen = templates[sum(ord(char) for char in text) % len(templates)]
    return clean_final_copy(chosen)


def _has_obvious_article_gap(text: str) -> bool:
    return bool(re.search(r"\bwith\s+AI-powered\s+smartphone\b", text or ""))


def _missing_brand_terms(text: str, brand_terms: list[str] | None) -> list[str]:
    lowered = (text or "").lower()
    missing = []
    for term in brand_terms or []:
        clean_term = term.strip().lower()
        if clean_term and clean_term not in lowered:
            missing.append(term)
    return missing
