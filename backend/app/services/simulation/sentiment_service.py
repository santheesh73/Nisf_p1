from app.core.config import get_settings
from app.providers.nlp.sentiment_provider import SentimentProvider
from app.schemas.simulation_schema import SentimentResult


class SentimentService:
    def __init__(self) -> None:
        self.provider = SentimentProvider(get_settings().sentiment_model)

    def analyze(self, text: str) -> SentimentResult:
        result = self.provider.analyze(text)
        return SentimentResult(label=result["label"], confidence=result["confidence"])
