from app.utils.text_utils import clamp


class EmotionScorer:
    def score(self, text: str, emotions: dict[str, float] | None = None, **kwargs) -> float:
        emotions = emotions or {}
        positive = emotions.get("joy", 0.0) + emotions.get("surprise", 0.0) * 0.5
        negative = sum(emotions.get(label, 0.0) for label in ["anger", "fear", "sadness", "disgust"])
        return clamp(55 + positive * 70 - negative * 45)
