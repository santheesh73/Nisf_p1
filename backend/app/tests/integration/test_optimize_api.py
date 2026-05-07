from fastapi.testclient import TestClient

from app.core import rate_limit as rate_limit_module
from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rate_limit_returns_429(monkeypatch):
    monkeypatch.setattr(
        rate_limit_module.RateLimiter,
        "_limits",
        lambda self: {"score": (2, 3600)},
    )
    rate_limit_module._rate_limiter = None
    client = TestClient(app)
    payload = {
        "text": "Build smarter campaigns with AI-powered insight.",
        "content_type": "ad",
        "tone": "clear",
        "platform": "web",
    }

    assert client.post("/api/v1/score", json=payload).status_code == 200
    assert client.post("/api/v1/score", json=payload).status_code == 200
    response = client.post("/api/v1/score", json=payload)

    assert response.status_code == 429
    assert response.json()["error"]["code"] == "rate_limit_exceeded"
    rate_limit_module._rate_limiter = None
