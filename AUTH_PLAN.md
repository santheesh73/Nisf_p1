# NISF Auth and User Ownership Plan

## Recommended MVP Strategy

Use JWT bearer authentication for production.

- Backend validates bearer tokens and extracts `user_id`.
- `optimization_jobs` and `feedback_metrics` store `user_id`.
- `GET /api/v1/jobs/*`, `GET /api/v1/history`, `POST /api/v1/generate/text`, `POST /api/v1/optimize`, and `POST /api/v1/feedback` require auth in production.
- `GET /health` and `GET /api/v1/health` remain public.

## Local Development Policy

Local mode may continue without auth for demo and development workflows. Production should not expose the write or history endpoints without auth.

## Backend Changes Required

- Add auth dependency that reads `Authorization: Bearer <token>`.
- Resolve `user_id` from the token.
- Persist `user_id` on jobs and feedback records.
- Filter history and job reads by `user_id`.
- Add sparse indexes on `user_id` for future rollout. Those placeholder indexes are already safe to keep.

## Frontend Changes Required

- Add login/session storage.
- Attach bearer token to `apiClient`.
- Handle `401` and `403` with a login or session-expired UI state.

## Production Blocker

Public deployment without auth is not recommended. Treat authentication and ownership enforcement as a blocker for internet-facing release.
