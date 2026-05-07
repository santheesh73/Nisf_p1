from pydantic import BaseModel, ConfigDict, Field


class ScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=12000)
    content_type: str = "marketing"
    tone: str = "clear"
    platform: str = "web"
    brand_terms: list[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    clarity: float
    engagement: float
    emotional_resonance: float
    readability: float
    originality: float
    brand_fit: float
    safety: float
    attention_coefficient: float
