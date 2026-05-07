from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery(
    "nisf",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.optimization_tasks", "app.workers.scoring_tasks", "app.workers.feedback_tasks"],
)
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
