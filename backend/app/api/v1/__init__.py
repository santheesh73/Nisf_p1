from fastapi import APIRouter

from app.api.v1 import auth, feedback, generate, health, history, jobs, optimize, score, templates

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(optimize.router)
api_router.include_router(score.router)
api_router.include_router(jobs.router)
api_router.include_router(templates.router)
api_router.include_router(feedback.router)
api_router.include_router(generate.router)
api_router.include_router(history.router)
