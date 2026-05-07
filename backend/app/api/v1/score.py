from fastapi import APIRouter, Depends, Request

from app.core.rate_limit import protect_endpoint
from app.core.auth import CurrentUser, get_current_user
from app.schemas.score_schema import ScoreBreakdown, ScoreRequest
from app.services.scoring import ScoringService
from app.services.simulation import SimulationService

router = APIRouter(prefix="/score", tags=["score"])


@router.post("", response_model=ScoreBreakdown)
def score_text(
    payload: ScoreRequest,
    _: Request,
    __: None = Depends(protect_endpoint("score")),
    _current_user: CurrentUser = Depends(get_current_user),
) -> ScoreBreakdown:
    simulation = SimulationService().simulate(payload.text)
    return ScoringService().score_text(
        payload.text,
        content_type=payload.content_type,
        tone=payload.tone,
        platform=payload.platform,
        emotions=simulation.emotions,
        brand_terms=payload.brand_terms,
    )
