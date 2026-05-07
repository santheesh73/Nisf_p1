import pytest
from pydantic import ValidationError

from app.schemas.generate_schema import GenerateTextRequest
from app.schemas.optimize_schema import OptimizeRequest
from app.schemas.score_schema import ScoreRequest


def test_optimize_request_requires_text_or_brief():
    with pytest.raises(ValidationError):
        OptimizeRequest()


def test_generate_request_rejects_unknown_input_text_field():
    with pytest.raises(ValidationError):
        GenerateTextRequest(input_text="hello", brief="brief")


def test_score_request_rejects_audience_object():
    with pytest.raises(ValidationError):
        ScoreRequest(
            text="hello",
            content_type="ad_copy",
            tone="persuasive",
            platform="instagram",
            audience={"region": "IN"},
        )


def test_generate_request_accepts_brand_terms_array_and_variant_bounds():
    payload = GenerateTextRequest(
        text="Boost your mobile experience with our AI-powered smartphone.",
        content_type="ad_copy",
        tone="persuasive",
        platform="instagram",
        variant_count=5,
        brand_terms=["AI-powered", "smartphone"],
    )
    assert payload.variant_count == 5
    assert payload.brand_terms == ["AI-powered", "smartphone"]

    with pytest.raises(ValidationError):
        GenerateTextRequest(
            text="Boost your mobile experience with our AI-powered smartphone.",
            variant_count=6,
        )

    with pytest.raises(ValidationError):
        OptimizeRequest(
            text="Boost your mobile experience with our AI-powered smartphone.",
            variant_count=2,
        )
