from app.services.simulation import SimulationService


def test_simulation_fallback_shape():
    result = SimulationService().simulate("Discover smart growth with clear analytics.")
    assert result.sentiment.label in {"positive", "negative", "neutral"}
    assert "joy" in result.emotions
    assert "neutral" in result.emotions
