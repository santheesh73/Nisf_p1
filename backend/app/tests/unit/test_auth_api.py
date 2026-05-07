from fastapi.testclient import TestClient

from app.api.v1 import auth as auth_api
from app.api.v1 import feedback as feedback_api
from app.api.v1 import history as history_api
from app.api.v1 import optimize as optimize_api
from app.core import auth as core_auth
from app.core.config import get_settings
from app.core.exceptions import NotFoundError
from app.main import app


class MemoryUserService:
    users_by_email = {}
    users_by_id = {}

    def create_user(self, *, email, password_hash, name):
        doc = {
            "_id": f"user-{len(self.users_by_id) + 1}",
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "is_active": True,
        }
        self.users_by_email[email] = doc
        self.users_by_id[doc["_id"]] = doc
        return doc

    def get_by_email(self, email):
        return self.users_by_email.get(email)

    def get_by_id(self, user_id):
        return self.users_by_id.get(user_id)

    def public_user(self, user):
        return {"id": user["_id"], "email": user["email"], "name": user["name"]}


def _configure_auth(monkeypatch):
    settings = get_settings()
    settings.auth_enabled = True
    settings.jwt_secret_key = "test-secret"
    settings.app_env = "local"
    MemoryUserService.users_by_email = {}
    MemoryUserService.users_by_id = {}
    monkeypatch.setattr(auth_api, "UserService", MemoryUserService)
    monkeypatch.setattr(core_auth, "UserService", MemoryUserService)
    return TestClient(app)


def _register(client, email="user@example.com", name="User Name"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "StrongPassword123", "name": name},
    )


def test_register_user_works(monkeypatch):
    client = _configure_auth(monkeypatch)
    response = _register(client)
    assert response.status_code == 200
    body = response.json()
    assert body["user"] == {"id": "user-1", "email": "user@example.com", "name": "User Name"}
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert "password_hash" not in body["user"]


def test_duplicate_email_rejected(monkeypatch):
    client = _configure_auth(monkeypatch)
    assert _register(client).status_code == 200
    response = _register(client)
    assert response.status_code == 409


def test_login_works_and_wrong_password_rejected(monkeypatch):
    client = _configure_auth(monkeypatch)
    _register(client)
    ok = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "StrongPassword123"})
    bad = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "wrong"})
    assert ok.status_code == 200
    assert ok.json()["access_token"]
    assert bad.status_code == 401


def test_auth_me_works_with_token(monkeypatch):
    client = _configure_auth(monkeypatch)
    token = _register(client).json()["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_protected_endpoint_rejects_no_token(monkeypatch):
    client = _configure_auth(monkeypatch)
    response = client.post(
        "/api/v1/generate/text",
        json={"text": "Build smarter campaigns.", "content_type": "ad", "tone": "clear", "platform": "web"},
    )
    assert response.status_code == 401


def test_optimize_stores_user_id(monkeypatch):
    client = _configure_auth(monkeypatch)
    token = _register(client).json()["access_token"]
    captured = {}

    class FakeJobService:
        def create_job(self, payload, user_id=None):
            captured["user_id"] = user_id
            return {"_id": "job-1", "status": "queued"}

    class FakeTask:
        def delay(self, job_id):
            captured["delayed"] = job_id

    monkeypatch.setattr(optimize_api, "JobService", FakeJobService)
    monkeypatch.setattr(optimize_api, "_celery_broker_available", lambda: True)
    monkeypatch.setattr(optimize_api, "run_text_optimization", FakeTask())
    response = client.post(
        "/api/v1/optimize",
        headers={"Authorization": f"Bearer {token}"},
        json={"brief": "Promote NISF", "content_type": "ad"},
    )
    assert response.status_code == 200
    assert captured == {"user_id": "user-1", "delayed": "job-1"}


def test_history_only_returns_current_user_jobs(monkeypatch):
    client = _configure_auth(monkeypatch)
    token = _register(client).json()["access_token"]
    captured = {}

    class FakeHistoryService:
        def list_jobs(self, **kwargs):
            captured.update(kwargs)
            return {"items": [], "count": 0}

    monkeypatch.setattr(history_api, "HistoryService", FakeHistoryService)
    response = client.get("/api/v1/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert captured["user_id"] == "user-1"


def test_feedback_attaches_user_id(monkeypatch):
    client = _configure_auth(monkeypatch)
    token = _register(client).json()["access_token"]
    captured = {}

    class FakeJobService:
        def get_job_for_user(self, job_id, user_id):
            captured["checked"] = (job_id, user_id)
            return {"_id": job_id, "user_id": user_id}

    class FakeFeedbackService:
        def record(self, payload, user_id=None):
            captured["recorded"] = user_id
            return {
                "id": "feedback-1",
                "user_id": user_id,
                "job_id": payload.job_id,
                "variant_id": payload.variant_id,
                "platform": payload.platform,
                "impressions": payload.impressions,
                "clicks": payload.clicks,
                "likes": payload.likes,
                "shares": payload.shares,
                "conversions": payload.conversions,
                "ctr": 0,
                "conversion_rate": 0,
            }

    monkeypatch.setattr(feedback_api, "JobService", FakeJobService)
    monkeypatch.setattr(feedback_api, "FeedbackService", FakeFeedbackService)
    response = client.post(
        "/api/v1/feedback",
        headers={"Authorization": f"Bearer {token}"},
        json={"job_id": "job-1", "variant_id": "v1"},
    )
    assert response.status_code == 200
    assert captured["checked"] == ("job-1", "user-1")
    assert captured["recorded"] == "user-1"


def test_user_cannot_access_another_users_job_result(monkeypatch):
    client = _configure_auth(monkeypatch)
    token = _register(client, email="owner@example.com").json()["access_token"]

    class FakeJobService:
        def get_job_for_user(self, job_id, user_id):
            raise NotFoundError(f"Job {job_id} was not found")

    from app.api.v1 import jobs as jobs_api

    monkeypatch.setattr(jobs_api, "JobService", FakeJobService)
    response = client.get("/api/v1/jobs/job-owned-by-other/result", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
