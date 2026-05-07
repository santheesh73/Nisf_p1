"""
Job service — CRUD operations for optimization jobs backed by MongoDB.

All functions use synchronous PyMongo so they work both inside FastAPI
(sync endpoints) and Celery workers without an event-loop.
"""

import uuid
from datetime import datetime, timezone
import logging

from app.core.constants import JobStatus
from app.core.exceptions import NotFoundError
from app.db.mongo import OPTIMIZATION_JOBS, get_sync_collection
from app.schemas.optimize_schema import OptimizeRequest

logger = logging.getLogger(__name__)


class JobService:
    """Manages the optimization_jobs collection in MongoDB."""

    def _collection(self):
        return get_sync_collection(OPTIMIZATION_JOBS)

    # --------------------------------------------------------------------- #
    # Create
    # --------------------------------------------------------------------- #

    def create_job(self, request: OptimizeRequest, user_id: str | None = None) -> dict:
        """Insert a new optimization job and return the document."""
        now = datetime.now(timezone.utc).isoformat()
        doc = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "status": JobStatus.QUEUED.value,
            "input": {
                "text": request.text,
                "brief": request.brief,
                "content_type": request.content_type,
                "tone": request.tone,
                "platform": request.platform,
                "brand_terms": request.brand_terms or [],
            },
            "config": {
                "max_iterations": request.max_iterations,
                "target_score": request.target_score,
                "convergence_threshold": request.convergence_threshold,
                "variant_count": request.variant_count,
            },
            "provider": "local",
            "model": "nisf-deterministic-local",
            "variants": [],
            "critic_directives": [],
            "iteration_history": [],
            "best_variant_id": None,
            "scores": None,
            "error_message": None,
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
        }
        self._collection().insert_one(doc)
        return doc

    # --------------------------------------------------------------------- #
    # Read
    # --------------------------------------------------------------------- #

    def get_job(self, job_id: str) -> dict:
        """Fetch a job by _id.  Raises NotFoundError if missing."""
        doc = self._collection().find_one({"_id": job_id})
        if doc is None:
            raise NotFoundError(f"Job {job_id} was not found")
        return doc

    def get_job_for_user(self, job_id: str, user_id: str | None) -> dict:
        """Fetch a user-owned job. Missing or wrong-owner jobs return the same 404."""
        query = {"_id": job_id}
        if user_id is not None:
            query["user_id"] = user_id
        doc = self._collection().find_one(query)
        if doc is None:
            raise NotFoundError(f"Job {job_id} was not found")
        return doc

    def get_job_status(self, job_id: str, user_id: str | None = None) -> dict:
        """Return a lightweight status view."""
        doc = self.get_job_for_user(job_id, user_id) if user_id is not None else self.get_job(job_id)
        return {
            "job_id": doc["_id"],
            "status": doc["status"],
            "error": doc.get("error_message"),
        }

    def get_job_result(self, job_id: str) -> dict:
        """Return the full job document (used by ResultService)."""
        return self.get_job(job_id)

    # --------------------------------------------------------------------- #
    # Update
    # --------------------------------------------------------------------- #

    def update_job_status(
        self, job_id: str, status: JobStatus | str, error: str | None = None
    ) -> None:
        """Set the job status and optionally an error message."""
        status_value = status.value if isinstance(status, JobStatus) else status
        update: dict = {
            "status": status_value,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        if error is not None:
            update["error_message"] = error
        if status_value == JobStatus.COMPLETED.value:
            update["completed_at"] = datetime.now(timezone.utc).isoformat()
        result = self._collection().update_one({"_id": job_id}, {"$set": update})
        if result.matched_count == 0:
            raise NotFoundError(f"Job {job_id} was not found")
        logger.info("job_status_updated", extra={"job_id": job_id, "stage": "optimization", "status": status_value})

    def save_job_result(self, job_id: str, result_data: dict) -> None:
        """Persist variants, scores, directives, and history into the job doc."""
        update: dict = {
            "variants": result_data.get("variants", []),
            "critic_directives": result_data.get("critic_directives", []),
            "iteration_history": result_data.get("iteration_history", []),
            "best_variant_id": result_data.get("best_variant_id"),
            "scores": result_data.get("scores"),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._collection().update_one({"_id": job_id}, {"$set": update})

    # --------------------------------------------------------------------- #
    # Failure
    # --------------------------------------------------------------------- #

    def mark_failed(self, job_id: str, error: str) -> None:
        """Mark a job as failed with an error message."""
        self.update_job_status(job_id, JobStatus.FAILED, error=error)
