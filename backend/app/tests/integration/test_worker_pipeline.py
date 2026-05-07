from app.pipelines.text import TextPipeline
from app.schemas.optimize_schema import OptimizeRequest


def test_text_pipeline_optimizes_locally():
    result = TextPipeline().optimize(
        OptimizeRequest(
            text="Launch our AI analytics platform.",
            platform="linkedin",
            max_iterations=1,
        )
    )
    assert result["best_variant"] is not None
    assert len(result["variants"]) >= 3
