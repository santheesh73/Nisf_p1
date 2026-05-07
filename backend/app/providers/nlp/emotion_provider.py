class EmotionProvider:
    labels = ["joy", "anger", "fear", "sadness", "disgust", "surprise", "neutral"]

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name
        self._pipeline = None
        import os

        try:
            from transformers import pipeline

            if model_name and os.getenv("ENABLE_TRANSFORMERS", "false").lower() == "true":
                self._pipeline = pipeline("text-classification", model=model_name, top_k=None)
        except Exception:
            self._pipeline = None

    def analyze(self, text: str) -> dict[str, float]:
        if self._pipeline:
            raw = self._pipeline(text[:512])[0]
            scores = {item["label"].lower(): round(float(item["score"]), 3) for item in raw}
            return {label: scores.get(label, 0.0) for label in self.labels}
        lowered = text.lower()
        scores = dict.fromkeys(self.labels, 0.05)
        if any(word in lowered for word in ["discover", "growth", "smart", "confidence", "win"]):
            scores["joy"] = 0.48
        if any(word in lowered for word in ["urgent", "limited", "now", "today"]):
            scores["surprise"] = 0.25
        if any(word in lowered for word in ["risk", "fear", "problem"]):
            scores["fear"] = 0.28
        scores["neutral"] = max(0.1, 1.0 - sum(v for k, v in scores.items() if k != "neutral"))
        return {key: round(value, 3) for key, value in scores.items()}
