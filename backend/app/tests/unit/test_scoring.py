from app.services.scoring import ScoringService
from app.utils.text_quality import has_awkward_phrases, instagram_persuasive_quality_bonus, is_dirty_final_copy


def test_scoring_engine_returns_bounded_scores():
    score = ScoringService().score_text(
        "Discover faster campaign insights with clear AI analytics. Start today.",
        emotions={"joy": 0.4, "surprise": 0.2, "anger": 0.0, "fear": 0.0, "sadness": 0.0, "disgust": 0.0},
    )
    assert 0 <= score.attention_coefficient <= 100
    assert 0 <= score.clarity <= 100
    assert score.safety == 100


def test_scoring_penalizes_awkward_ad_copy():
    bad_copy = (
        "Young days move fast, and your mobile experience should too with our AI-powered smartphone "
        "built for smart daily help, faster tasks, and smooth scrolling. Ready to discover the upgrade "
        "that helps you start faster every day?"
    )

    score = ScoringService().score_text(
        bad_copy,
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
    )

    assert has_awkward_phrases(bad_copy)
    assert is_dirty_final_copy(
        bad_copy,
        ["AI-powered", "smartphone", "mobile experience"],
        "ad_copy",
        "persuasive",
        "instagram",
    )
    assert score.attention_coefficient < 65


def test_scoring_rewards_natural_instagram_ad_copy():
    good_copy = (
        "Your day moves fast. Your phone should too. Capture sharper photos, finish tasks faster, "
        "and enjoy a smoother mobile experience with an AI-powered smartphone built for everyday momentum. "
        "Tap to explore today."
    )

    score = ScoringService().score_text(
        good_copy,
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
    )

    assert not is_dirty_final_copy(
        good_copy,
        ["AI-powered", "smartphone", "mobile experience"],
        "ad_copy",
        "persuasive",
        "instagram",
    )
    assert score.attention_coefficient > 70


def test_scoring_rewards_optimized_smartphone_instagram_ad_with_emotion_context():
    good_copy = (
        "Upgrade every scroll, shot, and task with our AI-powered smartphone built for sharper photos, "
        "smoother days, and faster productivity. Tap to discover your smarter mobile experience."
    )

    score = ScoringService().score_text(
        good_copy,
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        emotions={"joy": 0.5, "surprise": 0.2, "anger": 0.0, "fear": 0.0, "sadness": 0.0, "disgust": 0.0},
        brand_terms=["AI-powered", "smartphone", "mobile experience"],
    )

    assert score.attention_coefficient >= 85


def test_instagram_quality_bonus_prefers_lifestyle_hook_over_functional_hook():
    functional = (
        "Make every tap feel quicker with our AI-powered smartphone built for faster tasks, "
        "smooth scrolling, and sharp photos. Tap to explore today."
    )
    stronger = (
        "From work mode to weekend shots, move faster with an AI-powered smartphone built for sharp photos, "
        "smooth scrolling, and effortless everyday productivity. Tap to explore today."
    )
    kwargs = {
        "brand_terms": ["AI-powered", "smartphone", "mobile experience"],
        "content_type": "ad_copy",
        "tone": "persuasive",
        "platform": "instagram",
    }

    assert instagram_persuasive_quality_bonus(stronger, **kwargs) > instagram_persuasive_quality_bonus(functional, **kwargs)
