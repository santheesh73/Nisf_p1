from pydantic import BaseModel

from app.schemas.critic_schema import CriticDirectiveSchema
from app.schemas.score_schema import ScoreBreakdown
from app.schemas.simulation_schema import SimulationResultSchema


class VariantOut(BaseModel):
    id: str | None = None
    iteration: int
    content: str
    source: str = "local"
    is_safe: bool = True
    score: ScoreBreakdown | None = None
    simulation: SimulationResultSchema | None = None
    critic_directives: list[CriticDirectiveSchema] = []
