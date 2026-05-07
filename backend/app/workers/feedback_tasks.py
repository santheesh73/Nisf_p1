from app.workers.celery_app import celery_app


@celery_app.task(name="feedback.process_feedback")
def process_feedback_task(feedback_id: str):
    return {"status": "noop", "feedback_id": feedback_id}
