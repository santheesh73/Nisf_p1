from app.workers.celery_app import celery_app


@celery_app.task
def score_text_task(text: str) -> dict:
    from app.services.scoring import ScoringService

    return ScoringService().score_text(text).model_dump()
