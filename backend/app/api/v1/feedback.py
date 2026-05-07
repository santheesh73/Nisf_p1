from fastapi import APIRouter, Depends, Request

from app.core.rate_limit import protect_endpoint
from app.core.auth import CurrentUser, get_current_user
from app.services.job_service import JobService
from app.schemas.feedback_schema import FeedbackMetricIn, FeedbackMetricOut
from app.services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackMetricOut)
def record_feedback(
    payload: FeedbackMetricIn,
    _: Request,
    __: None = Depends(protect_endpoint("feedback")),
    current_user: CurrentUser = Depends(get_current_user),
) -> FeedbackMetricOut:
    user_id = None if current_user.is_dev else current_user.id
    if payload.job_id and user_id is not None:
        JobService().get_job_for_user(payload.job_id, user_id)
    return FeedbackService().record(payload, user_id=user_id)
