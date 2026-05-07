from pydantic import BaseModel


class SentimentResult(BaseModel):
    label: str
    confidence: float


class SimulationResultSchema(BaseModel):
    sentiment: SentimentResult
    emotions: dict[str, float]
