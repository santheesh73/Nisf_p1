import pytest

from app.core.config import get_settings
from app.schemas.critic_schema import CriticDirectiveSchema
from app.services.generation import GenerationService
from app.utils.text_quality import clean_final_copy, has_awkward_phrases, has_internal_notes, has_repeated_phrases, polish_marketing_copy


@pytest.fixture(autouse=True)
def use_local_generation(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "local")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_local_generation_returns_requested_variant_count():
    variants = GenerationService().generate_variants(
        text="Launch AI analytics for small teams.",
        brief=None,
        content_type="ad",
        tone="confident",
        platform="linkedin",
        count=3,
    )
    assert len(variants) == 3
    assert all(any(term in variant.lower() for term in ["ai", "analytics", "teams"]) for variant in variants)


def test_local_generation_uses_distinct_marketing_angles_and_brand_terms():
    variants = GenerationService().generate_variants(
        text="Boost your mobile experience with our new AI-powered smartphone.",
        brief=None,
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        count=5,
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
    )
    assert len(variants) == 5
    assert len(set(variant.split(".")[0] for variant in variants)) == 5
    assert all(any(term in variant for term in ["AI-powered", "smartphone", "mobile experience"]) for variant in variants)
    assert all(len(variant.split()) <= 38 for variant in variants)
    assert all("Refined focus:" not in variant for variant in variants)
    assert all("improve engagement while preserving the core offer" not in variant.lower() for variant in variants)
    assert all(not has_internal_notes(variant) for variant in variants)
    banned = [
        "revolutionize your daily life",
        "unlock your potential",
        "take it to the next level",
        "smarter way to interact",
        "create and innovate",
    ]
    assert all(not any(phrase in variant.lower() for phrase in banned) for variant in variants)
    assert all(any(cta in variant.lower() for cta in ["tap", "discover", "explore", "upgrade", "today"]) for variant in variants)
    assert any("sharp photos" in variant.lower() or "sharper photos" in variant.lower() or "faster tasks" in variant.lower() or "smooth scrolling" in variant.lower() for variant in variants)
    assert all(not has_awkward_phrases(variant) for variant in variants)


def test_instagram_smartphone_polish_avoids_awkward_templates():
    polished = polish_marketing_copy(
        "Young days move fast, and your mobile experience should too with our AI-powered smartphone built for smart daily help, faster tasks, and smooth scrolling. Ready to discover the upgrade that helps you start faster every day?",
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
    )

    assert not has_awkward_phrases(polished)
    assert "AI-powered smartphone" in polished
    assert any(benefit in polished.lower() for benefit in ["sharper photos", "faster", "smooth"])
    assert "tap to" in polished.lower()


def test_instagram_smartphone_polish_adds_lifestyle_context_to_functional_copy():
    polished = polish_marketing_copy(
        "Make every tap feel quicker with our AI-powered smartphone built for faster tasks, smooth scrolling, and sharp photos. Tap to explore today.",
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
    )

    assert "make every tap feel quicker" not in polished.lower()
    assert any(phrase in polished.lower() for phrase in ["your day moves fast", "work mode to weekend shots", "every task, shot, and scroll"])


def test_local_generation_changes_output_by_tone():
    base_kwargs = {
        "text": "Boost your mobile experience with our new AI-powered smartphone.",
        "brief": None,
        "content_type": "ad_copy",
        "platform": "instagram",
        "count": 2,
        "brand_terms": ["AI-powered", "smartphone", "mobile experience"],
    }
    professional = GenerationService().generate_variants(tone="professional", **base_kwargs)
    friendly = GenerationService().generate_variants(tone="friendly", **base_kwargs)
    urgent = GenerationService().generate_variants(tone="urgent", **base_kwargs)

    assert professional != friendly
    assert friendly != urgent
    assert professional[0] != urgent[0]
    assert any(word in professional[0].lower() for word in ["discover", "explore", "reliable", "professional", "workflow"])
    assert any(word in friendly[0].lower() for word in ["discover", "meet", "easy", "smooth", "today"])
    assert any(word in urgent[0].lower() for word in ["now", "today", "upgrade", "discover"])


def test_critic_directives_do_not_enter_generated_copy():
    variants = GenerationService().generate_variants(
        text="Boost your mobile experience with our new AI-powered smartphone.",
        brief=None,
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        count=3,
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
        directives=[
            CriticDirectiveSchema(
                target_dimension="engagement",
                issue="CTA is weak.",
                rewrite_instruction="Improve engagement while preserving the core offer.",
                priority=1,
                risk_level="low",
            )
        ],
    )

    assert all("Refined focus:" not in variant for variant in variants)
    assert all("improve engagement" not in variant.lower() for variant in variants)
    assert all("preserving the core offer" not in variant.lower() for variant in variants)


def test_clean_final_copy_removes_internal_notes_and_repetition():
    dirty = (
        "Move faster with AI-powered smartphone and take control of mobile experience, "
        "Move faster, and take control. Tap to discover it today "
        "Refined focus: improve engagement while preserving the core offer."
    )
    clean = clean_final_copy(dirty)

    assert "Refined focus:" not in clean
    assert "improve engagement" not in clean.lower()
    assert "ai-powered smartphone" in clean.lower()
    assert not has_internal_notes(clean)
    assert not has_repeated_phrases(clean)


def test_clean_final_copy_replaces_generic_marketing_cliches():
    dirty = "Unlock your potential with a game-changing smartphone that will revolutionize your daily life."
    clean = clean_final_copy(dirty)

    assert "unlock your potential" not in clean.lower()
    assert "game-changing" not in clean.lower()
    assert "revolutionize your daily life" not in clean.lower()
    assert clean.endswith((".", "!", "?"))


def test_local_generation_stays_relevant_for_multiple_inputs():
    examples = [
        (
            "Upgrade your daily routine with our smart fitness watch - track health, calls, and workouts in one stylish device.",
            {"smart", "fitness", "watch", "health", "calls", "workouts"},
        ),
        (
            "Order meals fast with our food delivery app connecting you to local restaurants.",
            {"food", "delivery", "app", "meals", "restaurants"},
        ),
        (
            "Learn new skills with online courses, expert lessons, and flexible study plans.",
            {"learn", "skills", "online", "courses", "lessons"},
        ),
        (
            "Refresh your skincare routine with a hydrating serum for smoother, glowing skin.",
            {"skincare", "serum", "smoother", "glowing", "skin"},
        ),
        (
            "Book flights, hotels, and holiday packages on our travel booking website.",
            {"flights", "hotels", "travel", "booking", "website"},
        ),
    ]

    for source, expected_terms in examples:
        variants = GenerationService().generate_variants(
            text=source,
            brief=None,
            content_type="marketing",
            tone="clear",
            platform="web",
            count=3,
        )
        joined = " ".join(variants).lower()

        assert len(variants) == 3
        assert len(set(variants)) == 3
        assert "string helps you get less friction" not in joined
        assert sum(term in joined for term in expected_terms) >= 3
