from app.core.config import get_settings
from app.providers.nlp.emotion_provider import EmotionProvider


class EmotionService:
    def __init__(self) -> None:
        self.provider = EmotionProvider(get_settings().emotion_model)

    def analyze(self, text: str) -> dict[str, float]:
        return self.provider.analyze(text)
