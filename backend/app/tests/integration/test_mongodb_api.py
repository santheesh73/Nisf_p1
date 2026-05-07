"""
Integration tests for the MongoDB-backed NISF API.

These tests use the FastAPI TestClient and require a running MongoDB instance.
They exercise the full API surface: optimize, jobs, feedback, generate, score, templates.
"""

import pytest
from fastapi.testclient import TestClient

from app.db.mongo import get_sync_collection, OPTIMIZATION_JOBS, FEEDBACK_METRICS
from app.main import app

client = TestClient(app)


# ────────────────────────────────────────────────────────────────────────────
# Health
# ────────────────────────────────────────────────────────────────────────────

def test_root_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_api_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ────────────────────────────────────────────────────────────────────────────
# MongoDB Connection
# ────────────────────────────────────────────────────────────────────────────

def test_mongodb_connection():
    """Verify the sync PyMongo driver can reach MongoDB."""
    col = get_sync_collection(OPTIMIZATION_JOBS)
    # insert + delete a throwaway doc
    col.insert_one({"_id": "__test_ping__", "test": True})
    doc = col.find_one({"_id": "__test_ping__"})
    assert doc is not None
    col.delete_one({"_id": "__test_ping__"})


# ────────────────────────────────────────────────────────────────────────────
# Optimize → Jobs flow
# ────────────────────────────────────────────────────────────────────────────

def test_optimize_creates_job_in_mongodb():
    """POST /api/v1/optimize should create a job document in MongoDB."""
    payload = {
        "text": "Launch our AI analytics platform for small teams.",
        "content_type": "ad",
        "tone": "confident",
        "platform": "linkedin",
    }
    r = client.post("/api/v1/optimize", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "job_id" in body
    assert body["status"] in ("queued", "completed", "running")

    # Verify in MongoDB
    col = get_sync_collection(OPTIMIZATION_JOBS)
    doc = col.find_one({"_id": body["job_id"]})
    assert doc is not None
    assert doc["input"]["text"] == payload["text"]


def test_job_status_returns_status():
    """GET /api/v1/jobs/{job_id}/status should return the job status."""
    payload = {"brief": "Promote an AI tool", "content_type": "ad"}
    r = client.post("/api/v1/optimize", json=payload)
    job_id = r.json()["job_id"]

    r2 = client.get(f"/api/v1/jobs/{job_id}/status")
    assert r2.status_code == 200
    body = r2.json()
    assert body["job_id"] == job_id
    assert "status" in body


def test_job_result_returns_completed_result():
    """GET /api/v1/jobs/{job_id}/result should return the full result."""
    payload = {
        "brief": "Promote an AI campaign tool to startup founders.",
        "tone": "direct",
        "platform": "web",
        "max_iterations": 2,
    }
    r = client.post("/api/v1/optimize", json=payload)
    job_id = r.json()["job_id"]

    r2 = client.get(f"/api/v1/jobs/{job_id}/result")
    assert r2.status_code == 200
    body = r2.json()
    assert body["job_id"] == job_id
    assert body["status"] in ("completed", "queued", "running", "failed")


def test_fake_job_id_returns_404():
    """Non-existent job should return 404."""
    r = client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000/status")
    assert r.status_code == 404

    r2 = client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000/result")
    assert r2.status_code == 404


# ────────────────────────────────────────────────────────────────────────────
# Feedback
# ────────────────────────────────────────────────────────────────────────────

def test_feedback_stores_in_mongodb():
    """POST /api/v1/feedback should persist a feedback document."""
    payload = {
        "job_id": "test-job-001",
        "variant_id": "v1",
        "platform": "linkedin",
        "impressions": 1000,
        "clicks": 50,
        "likes": 20,
        "shares": 5,
        "conversions": 10,
    }
    r = client.post("/api/v1/feedback", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["job_id"] == "test-job-001"
    assert body["ctr"] == pytest.approx(0.05)
    assert body["conversion_rate"] == pytest.approx(0.01)

    # Verify in MongoDB
    col = get_sync_collection(FEEDBACK_METRICS)
    doc = col.find_one({"_id": body["id"]})
    assert doc is not None
    assert doc["platform"] == "linkedin"


# ────────────────────────────────────────────────────────────────────────────
# Generate / Score / Templates  (no DB dependency)
# ────────────────────────────────────────────────────────────────────────────

def test_generate_text_still_works():
    """POST /api/v1/generate/text should return variants."""
    payload = {
        "text": "Build smarter campaigns with AI-powered insight.",
        "content_type": "ad",
        "tone": "clear",
        "platform": "web",
    }
    r = client.post("/api/v1/generate/text", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "variants" in body
    assert len(body["variants"]) > 0


def test_score_still_works():
    """POST /api/v1/score should return a score breakdown."""
    payload = {
        "text": "Build smarter campaigns with AI-powered insight.",
        "content_type": "ad",
        "tone": "clear",
        "platform": "web",
    }
    r = client.post("/api/v1/score", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "clarity" in body
    assert "engagement" in body


def test_templates_still_works():
    """GET /api/v1/templates should return template list."""
    r = client.get("/api/v1/templates")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) > 0
