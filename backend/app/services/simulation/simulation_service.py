from app.schemas.simulation_schema import SimulationResultSchema
from app.services.simulation.emotion_service import EmotionService
from app.services.simulation.sentiment_service import SentimentService


class SimulationService:
    def __init__(self) -> None:
        self.sentiment = SentimentService()
        self.emotion = EmotionService()

    def simulate(self, text: str) -> SimulationResultSchema:
        return SimulationResultSchema(
            sentiment=self.sentiment.analyze(text),
            emotions=self.emotion.analyze(text),
        )
