# NISF Frontend

React/Vite frontend for NISF Text Engine v1.

## Setup

```powershell
cd frontend/FRONTEND1/FRONTEND/FRONTEND/frontend
npm install
npm run dev -- --port 5173
```

This nested directory is the active frontend root. The top-level `frontend` directory is not the Vite app root.

The frontend targets:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
# Production example:
# VITE_API_BASE_URL=https://your-backend-domain.com
```

In development, Vite proxies `/health` and `/api/v1/*` to the backend.

## API Contract

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

## Valid Requests

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

Optimize selected variant:

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

Generate `variant_count` is clamped to `1..5`. Optimize `variant_count` is clamped to `3..5` to match the backend schema.

## Workflow

Generate Text calls `/api/v1/generate/text`, Optimize starts `/api/v1/optimize`, Job Progress polls `/api/v1/jobs/{job_id}/status`, Job Result loads `/api/v1/jobs/{job_id}/result`, and History loads `/api/v1/history` with localStorage fallback.

## Build

```powershell
npm run build
```

The frontend uses `apiClient` for backend requests and does not embed backend API keys in the browser bundle.
