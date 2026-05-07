# NISF Backend

FastAPI backend for the Neuro-Iterative Synthesis Framework. Text Engine v1 supports text generation, scoring, optimization jobs, progress polling, results, templates, feedback, and MongoDB-backed job history.

## Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Environment

MongoDB is the active runtime database.

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=nisf
```

Real LLM generation uses Groq when configured:

```env
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=
```

Local deterministic fallback:

```env
LLM_PROVIDER=local
LOCAL_MODEL=nisf-deterministic-local
```

Fallback policy:

```env
ALLOW_LLM_FALLBACK=true
GROQ_TIMEOUT_SECONDS=20
GROQ_MAX_RETRIES=1
MAX_REQUEST_BYTES=20000
```

Redis/Celery is optional unless async workers are required.

## Run

Windows-safe audit/local command:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If your virtual environment is named `.venv`, use `.\.venv\Scripts\Activate.ps1`.

Dev reload, optional:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

If `--reload` causes `PermissionError: [WinError 5] Access is denied` on Windows or OneDrive paths, run without `--reload`.

MongoDB:

```text
mongodb://localhost:27017
DB: nisf
```

Celery worker, optional:

```powershell
celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```

## Endpoints

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

## Valid Payloads

Generate text:

```json
{
  "text": "Our AI-powered smartphone helps users work faster, capture sharper photos, and enjoy smoother everyday performance.",
  "brief": "Create a persuasive Instagram ad copy for young professionals in India.",
  "content_type": "ad_copy",
  "tone": "persuasive",
  "platform": "instagram",
  "variant_count": 5,
  "brand_terms": ["AI-powered", "smartphone", "mobile experience"]
}
```

Optimize selected copy:

```json
{
  "text": "Your selected generated variant text here.",
  "brief": "Create a persuasive Instagram ad copy for young professionals in India.",
  "content_type": "ad_copy",
  "tone": "persuasive",
  "platform": "instagram",
  "max_iterations": 3,
  "target_score": 85,
  "convergence_threshold": 2,
  "variant_count": 5,
  "brand_terms": ["AI-powered", "smartphone", "mobile experience"]
}
```

Score only:

```json
{
  "text": "Upgrade every scroll, shot, and task with an AI-powered smartphone built for sharper photos and smoother days.",
  "content_type": "ad_copy",
  "tone": "persuasive",
  "platform": "instagram",
  "brand_terms": ["AI-powered", "smartphone", "mobile experience"]
}
```

History:

```text
GET /api/v1/history?limit=20&status=completed&platform=instagram
```

## Workflow

User enters text and brief, frontend calls `POST /api/v1/generate/text`, variants are displayed, selected variant is sent to `POST /api/v1/optimize`, frontend polls `/api/v1/jobs/{job_id}/status`, then renders `/api/v1/jobs/{job_id}/result`.

## MongoDB Collections

| Collection | Purpose |
|---|---|
| `optimization_jobs` | Job input, status, variants, scores, result history |
| `templates` | Prompt templates |
| `feedback_metrics` | Post-deployment performance feedback |
| `model_registry` | Reserved model metadata |

## Tests

```powershell
pytest
```

MongoDB should be running for integration tests that touch persistence.

## Docker Compose

The root `docker-compose.yml` defines MongoDB, Redis, backend, and frontend services. The backend uses container-network URLs for MongoDB and Redis. The frontend is served on `http://localhost:5173` and calls the backend at `http://127.0.0.1:8000`.

## Production Notes

Keep `APP_ENV=production`, `DEBUG=false`, configure production `ALLOWED_ORIGINS`, and never expose backend API keys to the frontend. PostgreSQL settings may exist in legacy config, but MongoDB is the active runtime database for Text Engine v1.

Rate limiting is active for `generate`, `optimize`, `score`, and `feedback`. In local mode the limits are relaxed. In production the limits are tighter and return HTTP `429`.

MongoDB backup guidance:
- Prefer MongoDB Atlas backups for managed production deployments.
- For self-managed MongoDB, schedule `mongodump` and test restore with `mongorestore`.
- Keep restore instructions with deployment runbooks before public launch.

Authentication and user ownership are the main remaining production blocker if you plan to expose the app publicly. See [AUTH_PLAN.md](../AUTH_PLAN.md) and [DEPLOYMENT.md](../DEPLOYMENT.md).
