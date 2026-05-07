from pydantic import BaseModel

from app.schemas.critic_schema import CriticDirectiveSchema
from app.schemas.score_schema import ScoreBreakdown
from app.schemas.variant_schema import VariantOut


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    error: str | None = None


class IterationHistoryItem(BaseModel):
    iteration: int
    best_score: float
    improvement: float
    selected_variant: str | None = None
    stop_reason: str | None = None


class JobResultResponse(BaseModel):
    job_id: str
    status: str
    best_variant: VariantOut | None
    variants: list[VariantOut]
    scores: ScoreBreakdown | None = None
    critic_directives: list[CriticDirectiveSchema] = []
    iteration_history: list[dict]
    error: str | None = None
