from fastapi import APIRouter, Depends

from app.core.auth import CurrentUser, get_current_user
from app.schemas.job_schema import JobResultResponse, JobStatusResponse
from app.services.job_service import JobService
from app.services.result_service import ResultService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}/status", response_model=JobStatusResponse)
def get_job_status(job_id: str, current_user: CurrentUser = Depends(get_current_user)) -> JobStatusResponse:
    user_id = None if current_user.is_dev else current_user.id
    status = JobService().get_job_status(job_id, user_id=user_id)
    return JobStatusResponse(**status)


@router.get("/{job_id}/result", response_model=JobResultResponse)
def get_job_result(job_id: str, current_user: CurrentUser = Depends(get_current_user)) -> JobResultResponse:
    job_service = JobService()
    if current_user.is_dev:
        job_doc = job_service.get_job(job_id)
    else:
        job_doc = job_service.get_job_for_user(job_id, user_id=current_user.id)
    return ResultService().build_job_result(job_doc)
