# MongoDB exports (active database layer)
from app.db.mongo import (
    FEEDBACK_METRICS,
    MODEL_REGISTRY,
    OPTIMIZATION_JOBS,
    TEMPLATES,
    close_mongo,
    connect_mongo,
    get_collection,
    get_database,
    get_sync_collection,
    get_sync_database,
)

__all__ = [
    # MongoDB
    "connect_mongo",
    "close_mongo",
    "get_database",
    "get_collection",
    "get_sync_database",
    "get_sync_collection",
    "OPTIMIZATION_JOBS",
    "TEMPLATES",
    "FEEDBACK_METRICS",
    "MODEL_REGISTRY",
]

# Legacy SQLAlchemy exports are available via direct import from app.db.base / app.db.session
# but are NOT eagerly imported here to avoid requiring a PostgreSQL driver at startup.
