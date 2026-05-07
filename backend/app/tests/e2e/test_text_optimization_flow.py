from app.pipelines.text import TextPipeline
from app.schemas.optimize_schema import OptimizeRequest


def test_text_optimization_flow_returns_history_and_scores():
    result = TextPipeline().optimize(
        OptimizeRequest(
            brief="Promote an AI campaign tool to startup founders.",
            tone="direct",
            platform="web",
            max_iterations=2,
        )
    )
    best = result["best_variant"]
    assert best.score.attention_coefficient > 0
    assert result["iteration_history"]
