from app.core.constants import DEFAULT_SCORE_WEIGHTS
from app.utils.text_utils import clamp


def weighted_attention(scores: dict[str, float], weights: dict[str, float] | None = None) -> float:
    selected = weights or DEFAULT_SCORE_WEIGHTS
    return clamp(sum(scores.get(key, 0.0) * weight for key, weight in selected.items()))
