"""
Feedback service — stores performance feedback metrics in MongoDB.
"""

import uuid
from datetime import datetime, timezone

from app.db.mongo import FEEDBACK_METRICS, get_sync_collection
from app.schemas.feedback_schema import FeedbackMetricIn, FeedbackMetricOut


class FeedbackService:
    """Writes/reads the feedback_metrics MongoDB collection."""

    def _collection(self):
        return get_sync_collection(FEEDBACK_METRICS)

    def record(self, payload: FeedbackMetricIn, user_id: str | None = None) -> FeedbackMetricOut:
        impressions = payload.impressions
        ctr = payload.ctr if payload.ctr is not None else (payload.clicks / impressions if impressions else 0.0)
        conversion_rate = (
            payload.conversion_rate
            if payload.conversion_rate is not None
            else (payload.conversions / impressions if impressions else 0.0)
        )
        doc = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "job_id": payload.job_id,
            "variant_id": payload.variant_id,
            "platform": payload.platform,
            "impressions": payload.impressions,
            "clicks": payload.clicks,
            "likes": payload.likes,
            "shares": payload.shares,
            "conversions": payload.conversions,
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._collection().insert_one(doc)
        return FeedbackMetricOut(
            id=doc["_id"],
            user_id=doc["user_id"],
            job_id=doc["job_id"],
            variant_id=doc["variant_id"],
            platform=doc["platform"],
            impressions=doc["impressions"],
            clicks=doc["clicks"],
            likes=doc["likes"],
            shares=doc["shares"],
            conversions=doc["conversions"],
            ctr=doc["ctr"],
            conversion_rate=doc["conversion_rate"],
        )
