import logging

from fastapi import APIRouter, Depends, Request
from kombu.exceptions import KombuError

from app.core.rate_limit import protect_endpoint
from app.core.auth import CurrentUser, get_current_user
from app.schemas.optimize_schema import OptimizeRequest, OptimizeResponse
from app.services.job_service import JobService
from app.workers.celery_app import celery_app
from app.workers.optimization_tasks import execute_text_optimization, run_text_optimization

router = APIRouter(prefix="/optimize", tags=["optimize"])
logger = logging.getLogger(__name__)


@router.post("", response_model=OptimizeResponse)
def create_optimization_job(
    payload: OptimizeRequest,
    _: Request,
    __: None = Depends(protect_endpoint("optimize")),
    current_user: CurrentUser = Depends(get_current_user),
) -> OptimizeResponse:
    user_id = None if current_user.is_dev else current_user.id
    job_doc = JobService().create_job(payload, user_id=user_id)
    job_id = job_doc["_id"]
    if _celery_broker_available():
        run_text_optimization.delay(job_id)
    else:
        logger.warning("celery_broker_unavailable_local_fallback", extra={"job_id": job_id, "stage": "optimization"})
        execute_text_optimization(job_id)
        job_doc = JobService().get_job(job_id)
    return OptimizeResponse(job_id=job_id, status=job_doc["status"])


def _celery_broker_available() -> bool:
    try:
        with celery_app.connection_for_write() as connection:
            connection.ensure_connection(max_retries=0)
        return True
    except (KombuError, OSError):
        return False
