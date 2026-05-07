import logging

from app.db.mongo import FEEDBACK_METRICS, MODEL_REGISTRY, OPTIMIZATION_JOBS, TEMPLATES, USERS, get_database

logger = logging.getLogger(__name__)


async def ensure_mongo_indexes() -> None:
    """Create/verify MongoDB indexes without blocking app startup on failure."""
    try:
        db = get_database()
        jobs = db[OPTIMIZATION_JOBS]
        feedback = db[FEEDBACK_METRICS]
        templates = db[TEMPLATES]
        model_registry = db[MODEL_REGISTRY]
        users = db[USERS]

        await jobs.create_index("status")
        await jobs.create_index([("created_at", -1)])
        await jobs.create_index([("updated_at", -1)])
        await jobs.create_index([("completed_at", -1)])
        await jobs.create_index("input.content_type")
        await jobs.create_index("input.platform")
        await jobs.create_index("user_id", sparse=True)

        await feedback.create_index("job_id")
        await feedback.create_index("variant_id")
        await feedback.create_index("platform")
        await feedback.create_index([("created_at", -1)])
        await feedback.create_index("user_id", sparse=True)

        await templates.create_index("id", unique=True, sparse=True)
        await templates.create_index("content_type")

        await model_registry.create_index("provider", sparse=True)
        await model_registry.create_index("model", sparse=True)

        await users.create_index("email", unique=True)
        await users.create_index([("created_at", -1)])

        logger.info("mongodb_indexes_verified")
    except Exception as exc:
        logger.warning("mongodb_index_creation_failed", extra={"error": str(exc)})
