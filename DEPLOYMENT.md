# NISF Deployment Guide

## Recommended Stack

- Frontend: Vercel or Netlify
- Backend: Render, Railway, Fly.io, AWS, Azure, or GCP
- MongoDB: MongoDB Atlas
- Redis: Upstash, Redis Cloud, or another managed Redis

## Environment Variables

Backend:

- `APP_ENV`
- `DEBUG`
- `MONGODB_URL`
- `MONGODB_DB_NAME`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `LLM_PROVIDER`
- `GROQ_API_KEY`
- `GROQ_MODEL`
- `ALLOW_LLM_FALLBACK`
- `GROQ_TIMEOUT_SECONDS`
- `GROQ_MAX_RETRIES`
- `ALLOWED_ORIGINS`
- `MAX_REQUEST_BYTES`

Frontend:

- `VITE_API_BASE_URL`

## Deploy Order

1. Deploy MongoDB.
2. Deploy Redis.
3. Deploy backend.
4. Deploy frontend.

## Local Run

Backend:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend/FRONTEND1/FRONTEND/FRONTEND/frontend
npm install
npm run dev -- --port 5173
```

## Smoke Tests After Deploy

- `GET /health`
- `GET /api/v1/health`
- `POST /api/v1/generate/text`
- `POST /api/v1/score`
- `POST /api/v1/optimize`
- `GET /api/v1/jobs/{job_id}/status`
- `GET /api/v1/jobs/{job_id}/result`
- `GET /api/v1/history`
- `GET /api/v1/templates`
- `POST /api/v1/feedback`

## Secret Rotation

- Rotate `GROQ_API_KEY` in your provider dashboard and deployment platform.
- Redeploy backend after secret changes.
- Never expose backend secrets in frontend environment variables.

## Backup and Restore

- Prefer MongoDB Atlas backups in production.
- For self-managed MongoDB, schedule `mongodump`.
- Test `mongorestore` regularly in a non-production environment.

## Rollback Plan

- Keep the previous backend image/build available.
- Revert frontend deployment to the previous successful build.
- Restore MongoDB from the latest clean backup only when data corruption is confirmed.
