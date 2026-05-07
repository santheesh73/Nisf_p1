from fastapi.testclient import TestClient

from app.api.v1 import history as history_api
from app.main import app


def test_history_api_returns_service_payload(monkeypatch):
    class FakeHistoryService:
        def list_jobs(self, limit=20, status=None, content_type=None, platform=None):
            assert limit == 2
            assert status == "completed"
            assert content_type == "ad_copy"
            assert platform == "instagram"
            return {"items": [], "count": 0}

    monkeypatch.setattr(history_api, "HistoryService", FakeHistoryService)
    client = TestClient(app)

    response = client.get(
        "/api/v1/history",
        params={"limit": 2, "status": "completed", "content_type": "ad_copy", "platform": "instagram"},
    )

    assert response.status_code == 200
    assert response.json() == {"items": [], "count": 0}
