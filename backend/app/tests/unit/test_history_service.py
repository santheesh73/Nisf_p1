from app.services.history_service import HistoryService


class FakeCursor:
    def __init__(self, docs):
        self.docs = list(docs)

    def sort(self, field, direction):
        reverse = direction == -1
        self.docs.sort(key=lambda item: item.get(field) or "", reverse=reverse)
        return self

    def limit(self, limit):
        self.docs = self.docs[:limit]
        return self

    def __iter__(self):
        return iter(self.docs)


class FakeCollection:
    def __init__(self, docs):
        self.docs = docs
        self.last_query = None

    def find(self, query):
        self.last_query = query
        return FakeCursor(self.docs)


def test_history_service_returns_empty_history(monkeypatch):
    collection = FakeCollection([])
    monkeypatch.setattr(HistoryService, "_collection", lambda self: collection)

    result = HistoryService().list_jobs()

    assert result == {"items": [], "count": 0}


def test_history_service_builds_completed_job_preview(monkeypatch):
    collection = FakeCollection(
        [
            {
                "_id": "job-1",
                "status": "completed",
                "input": {"content_type": "ad_copy", "tone": "persuasive", "platform": "instagram"},
                "created_at": "2026-05-06T10:00:00Z",
                "updated_at": "2026-05-06T10:02:00Z",
                "completed_at": "2026-05-06T10:02:00Z",
                "best_variant_id": "v2",
                "scores": {"attention_coefficient": 86.5},
                "variants": [
                    {"id": "v1", "text": "First variant", "scores": {"attention_coefficient": 70}},
                    {"id": "v2", "text": "Best variant text for history", "scores": {"attention_coefficient": 86.5}},
                ],
            }
        ]
    )
    monkeypatch.setattr(HistoryService, "_collection", lambda self: collection)

    result = HistoryService().list_jobs(limit=20, status="completed", content_type="ad_copy", platform="instagram")

    assert collection.last_query == {
        "status": "completed",
        "input.content_type": "ad_copy",
        "input.platform": "instagram",
    }
    assert result["count"] == 1
    assert result["items"][0]["job_id"] == "job-1"
    assert result["items"][0]["attention_coefficient"] == 86.5
    assert result["items"][0]["best_variant_preview"] == "Best variant text for history"


def test_history_service_clamps_limit(monkeypatch):
    docs = [{"_id": f"job-{index}", "status": "queued", "created_at": str(index)} for index in range(150)]
    collection = FakeCollection(docs)
    monkeypatch.setattr(HistoryService, "_collection", lambda self: collection)

    result = HistoryService().list_jobs(limit=500)

    assert result["count"] == 100
