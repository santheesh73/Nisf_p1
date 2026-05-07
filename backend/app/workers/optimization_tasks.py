import logging
import time

from app.core.constants import JobStatus
from app.pipelines.text import TextPipeline
from app.schemas.optimize_schema import OptimizeRequest
from app.services.job_service import JobService
from app.services.result_service import ResultService
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, autoretry_for=(ConnectionError, TimeoutError), retry_backoff=True, retry_kwargs={"max_retries": 3})
def run_text_optimization(self, job_id: str) -> dict:
    return execute_text_optimization(job_id)


def execute_text_optimization(job_id: str) -> dict:
    """Run the full text-optimization pipeline and persist results in MongoDB."""
    jobs = JobService()
    results = ResultService()
    started = time.perf_counter()
    try:
        job_doc = jobs.get_job(job_id)
        jobs.update_job_status(job_id, JobStatus.RUNNING)

        inp = job_doc["input"]
        cfg = job_doc["config"]
        request = OptimizeRequest(
            text=inp.get("text"),
            brief=inp.get("brief"),
            content_type=inp.get("content_type", "marketing"),
            tone=inp.get("tone", "clear"),
            platform=inp.get("platform", "web"),
            max_iterations=cfg.get("max_iterations", 3),
            target_score=cfg.get("target_score", 85.0),
            convergence_threshold=cfg.get("convergence_threshold", 2.0),
            variant_count=cfg.get("variant_count", 4),
            brand_terms=inp.get("brand_terms", []),
        )

        jobs.update_job_status(job_id, JobStatus.OPTIMIZING)
        result = TextPipeline().optimize(
            request,
            stage_callback=lambda status: jobs.update_job_status(job_id, status),
        )

        results.persist_result(job_id, result)
        jobs.update_job_status(job_id, JobStatus.COMPLETED)
        logger.info(
            "optimization_completed",
            extra={
                "job_id": job_id,
                "stage": "optimization",
                "request_id": None,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            },
        )
        return {"job_id": job_id, "status": JobStatus.COMPLETED.value}
    except Exception as exc:
        logger.exception("optimization_failed", extra={"job_id": job_id, "stage": "optimization", "request_id": None})
        try:
            jobs.mark_failed(job_id, str(exc))
        finally:
            raise
