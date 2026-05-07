from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.api.v1.health import router as root_health_router
from app.core.config import find_unexpected_env_files, get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, request_logging_middleware
from app.db.indexes import ensure_mongo_indexes
from app.db.mongo import close_mongo, connect_mongo
from app.providers.llm import get_llm_provider

settings = get_settings()
configure_logging(settings.debug)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Startup / shutdown lifecycle — manages the MongoDB connection."""
    provider = get_llm_provider()
    unexpected_env_files = [str(path) for path in find_unexpected_env_files()]
    logger.info(
        "startup_llm_provider_selected",
        extra={
            "app_env": settings.app_env,
            "debug": settings.debug,
            "provider": provider.name,
            "selected_llm_provider": settings.llm_provider,
            "configured_model": getattr(provider, "model", None),
            "has_groq_key": bool(settings.groq_api_key),
        },
    )
    if unexpected_env_files:
        logger.warning("unexpected_env_files_detected", extra={"paths": unexpected_env_files})
    await connect_mongo()
    await ensure_mongo_indexes()
    yield
    await close_mongo()


app = FastAPI(title=settings.app_name, debug=settings.debug, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_logging_middleware)
register_exception_handlers(app)

app.include_router(root_health_router)
app.include_router(api_router, prefix="/api/v1")
