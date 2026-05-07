"""
MongoDB connection module using Motor async driver.

Provides connection management, database access, and collection helpers
for the NISF backend. Uses AsyncIOMotorClient for async operations and
PyMongo utilities for synchronous fallback (Celery workers).
"""

import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database as SyncDatabase

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singletons
# ---------------------------------------------------------------------------

_async_client: AsyncIOMotorClient | None = None
_async_db: AsyncIOMotorDatabase | None = None
_sync_client: MongoClient | None = None
_sync_db: SyncDatabase | None = None

# ---------------------------------------------------------------------------
# Collection names
# ---------------------------------------------------------------------------

OPTIMIZATION_JOBS = "optimization_jobs"
TEMPLATES = "templates"
FEEDBACK_METRICS = "feedback_metrics"
MODEL_REGISTRY = "model_registry"
USERS = "users"

# ---------------------------------------------------------------------------
# Async helpers (FastAPI lifespan)
# ---------------------------------------------------------------------------


async def connect_mongo() -> None:
    """Open the async Motor client and cache the database handle."""
    global _async_client, _async_db
    settings = get_settings()
    _async_client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    _async_db = _async_client[settings.mongodb_db_name]
    try:
        await _async_client.admin.command("ping")
        logger.info(
            "mongodb_connected",
            extra={"url": settings.mongodb_url, "db": settings.mongodb_db_name},
        )
    except Exception as exc:
        logger.error(
            "mongodb_connection_failed",
            extra={"error": str(exc)},
        )
        _async_client.close()
        _async_client = None
        _async_db = None
        raise RuntimeError(
            "MongoDB connection failed during startup. Check MONGODB_URL, ensure MongoDB is running, "
            "and confirm the configured database is reachable."
        ) from exc


async def close_mongo() -> None:
    """Close the async Motor client."""
    global _async_client, _async_db
    if _async_client is not None:
        _async_client.close()
        _async_client = None
        _async_db = None
        logger.info("mongodb_disconnected")


def get_database() -> AsyncIOMotorDatabase:
    """Return the cached async database handle."""
    if _async_db is None:
        raise RuntimeError("MongoDB is not initialised — call connect_mongo() first")
    return _async_db


def get_collection(name: str) -> Any:
    """Shortcut: ``get_collection(OPTIMIZATION_JOBS)``."""
    return get_database()[name]


# ---------------------------------------------------------------------------
# Sync helpers (Celery workers / fallback)
# ---------------------------------------------------------------------------


def get_sync_client() -> MongoClient:
    """Return (or create) a synchronous PyMongo client."""
    global _sync_client
    if _sync_client is None:
        settings = get_settings()
        _sync_client = MongoClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    return _sync_client


def get_sync_database() -> SyncDatabase:
    """Return (or create) a synchronous PyMongo database handle."""
    global _sync_db
    if _sync_db is None:
        settings = get_settings()
        _sync_db = get_sync_client()[settings.mongodb_db_name]
    return _sync_db


def get_sync_collection(name: str) -> Any:
    """Shortcut for synchronous collection access."""
    return get_sync_database()[name]
