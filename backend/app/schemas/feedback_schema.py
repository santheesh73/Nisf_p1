from pydantic import BaseModel, Field


class FeedbackMetricIn(BaseModel):
    job_id: str | None = None
    variant_id: str | None = None
    platform: str | None = None
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    conversions: int = Field(default=0, ge=0)
    ctr: float | None = Field(default=None, ge=0)
    conversion_rate: float | None = Field(default=None, ge=0)


class FeedbackMetricOut(FeedbackMetricIn):
    id: str
    user_id: str | None = None
