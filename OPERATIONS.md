# NISF Observability and Operations

## Current Logging

- Structured JSON logs
- Request IDs on HTTP responses
- Job IDs and optimization stage logs
- MongoDB connection and index verification logs
- Groq retry and fallback logs
- Rate limit event logs

## Monitoring Recommendations

- Uptime monitor for backend health endpoints
- Error tracking for backend exceptions
- Centralized log aggregation
- Frontend availability checks

## Metrics Wishlist

- Request latency by endpoint
- Optimization job duration
- Groq fallback count
- Failed job count
- Average attention score
- History endpoint latency

## Health Checks

- `GET /health`
- `GET /api/v1/health`

## Production Notes

- Do not log secrets.
- Do not log full prompts by default in production.
- Review rate-limit and Groq failure logs after launch week.
