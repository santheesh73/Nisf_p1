from app.schemas.score_schema import ScoreBreakdown
from app.utils.score_utils import weighted_attention


class CompositeScorer:
    def score(self, dimensions: dict[str, float]) -> ScoreBreakdown:
        payload = dict(dimensions)
        payload["attention_coefficient"] = weighted_attention(payload)
        return ScoreBreakdown(**payload)
