class SentimentProvider:
    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name
        self._pipeline = None
        import os

        try:
            from transformers import pipeline

            if model_name and os.getenv("ENABLE_TRANSFORMERS", "false").lower() == "true":
                self._pipeline = pipeline("sentiment-analysis", model=model_name)
        except Exception:
            self._pipeline = None

    def analyze(self, text: str) -> dict:
        if self._pipeline:
            raw = self._pipeline(text[:512])[0]
            label = raw["label"].lower()
            if label in {"pos", "positive"}:
                label = "positive"
            elif label in {"neg", "negative"}:
                label = "negative"
            else:
                label = "neutral"
            return {"label": label, "confidence": round(float(raw["score"]), 3)}
        positive = {"boost", "smart", "clear", "faster", "confidence", "discover", "win", "growth"}
        negative = {"risk", "fail", "slow", "confusing", "waste", "problem"}
        lowered = text.lower()
        pos = sum(word in lowered for word in positive)
        neg = sum(word in lowered for word in negative)
        if pos > neg:
            return {"label": "positive", "confidence": min(0.95, 0.55 + pos * 0.08)}
        if neg > pos:
            return {"label": "negative", "confidence": min(0.95, 0.55 + neg * 0.08)}
        return {"label": "neutral", "confidence": 0.62}
