from app.services.result_service import ResultService


def test_build_job_result_uses_best_variant_id_and_provider():
    service = ResultService()
    job_doc = {
        "_id": "job-123",
        "status": "completed",
        "best_variant_id": "v2",
        "critic_directives": [],
        "error_message": None,
        "iteration_history": [{"iteration": 0, "best_score": 86.34, "improvement": 86.34}],
        "variants": [
            {
                "id": "v1",
                "text": "Variant one",
                "iteration": 0,
                "metadata": {"provider": "groq", "content_type": "ad_copy", "tone": "persuasive", "platform": "instagram"},
                "scores": {"clarity": 90, "engagement": 70, "emotional_resonance": 80, "readability": 75, "originality": 85, "brand_fit": 82, "safety": 100, "attention_coefficient": 80.0},
                "simulation": None,
            },
            {
                "id": "v2",
                "text": "Variant two",
                "iteration": 0,
                "metadata": {"provider": "groq", "content_type": "ad_copy", "tone": "persuasive", "platform": "instagram"},
                "scores": {"clarity": 95, "engagement": 90, "emotional_resonance": 88, "readability": 74, "originality": 90, "brand_fit": 86, "safety": 100, "attention_coefficient": 86.34},
                "simulation": None,
            },
        ],
    }

    result = service.build_job_result(job_doc)

    assert result.best_variant is not None
    assert result.best_variant.id == "v2"
    assert result.best_variant.source == "groq"
    assert result.scores is not None
    assert result.scores.attention_coefficient == 86.34
