from app.db.mongo import OPTIMIZATION_JOBS, get_sync_collection


class HistoryService:
    """Builds lightweight job history views from optimization job documents."""

    def _collection(self):
        return get_sync_collection(OPTIMIZATION_JOBS)

    def list_jobs(
        self,
        limit: int = 20,
        status: str | None = None,
        content_type: str | None = None,
        platform: str | None = None,
        user_id: str | None = None,
    ) -> dict:
        safe_limit = min(max(int(limit or 20), 1), 100)
        query: dict = {}
        if user_id is not None:
            query["user_id"] = user_id
        if status:
            query["status"] = status
        if content_type:
            query["input.content_type"] = content_type
        if platform:
            query["input.platform"] = platform

        cursor = self._collection().find(query).sort("created_at", -1).limit(safe_limit)
        items = [self._history_item(job) for job in cursor]
        return {"items": items, "count": len(items)}

    def _history_item(self, job: dict) -> dict:
        job_input = job.get("input") or {}
        best_text = self._best_variant_text(job)
        return {
            "job_id": job.get("job_id") or job.get("_id"),
            "status": job.get("status"),
            "content_type": job_input.get("content_type") or job.get("content_type"),
            "tone": job_input.get("tone") or job.get("tone"),
            "platform": job_input.get("platform") or job.get("platform"),
            "created_at": job.get("created_at"),
            "updated_at": job.get("updated_at"),
            "completed_at": job.get("completed_at"),
            "attention_coefficient": self._attention_coefficient(job),
            "best_variant_preview": self._preview(best_text),
        }

    def _best_variant_text(self, job: dict) -> str | None:
        best_variant = job.get("best_variant")
        if isinstance(best_variant, dict):
            text = best_variant.get("content") or best_variant.get("text")
            if text:
                return text

        best_variant_id = job.get("best_variant_id")
        for variant in job.get("variants") or []:
            if variant.get("id") == best_variant_id or variant.get("is_best"):
                return variant.get("content") or variant.get("text")
        return None

    def _attention_coefficient(self, job: dict) -> float | None:
        candidates = [
            job.get("scores") or {},
            (job.get("best_variant") or {}).get("score") or {},
            (job.get("best_variant") or {}).get("scores") or {},
        ]
        best_variant_id = job.get("best_variant_id")
        for variant in job.get("variants") or []:
            if variant.get("id") == best_variant_id or variant.get("is_best"):
                candidates.append(variant.get("scores") or {})

        for candidate in candidates:
            value = candidate.get("attention_coefficient")
            if value is not None:
                return value
        return None

    def _preview(self, text: str | None) -> str | None:
        if not text:
            return None
        clean = " ".join(str(text).split())
        return clean if len(clean) <= 160 else f"{clean[:157]}..."
