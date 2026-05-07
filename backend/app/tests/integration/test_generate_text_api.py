import sys
import types

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


def test_generate_text_api_uses_groq_provider_when_configured(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["model"] == "llama-3.3-70b-versatile"
            message = types.SimpleNamespace(
                content='["Move faster with NISF-built copy.", "Turn ideas into polished campaigns."]'
            )
            choice = types.SimpleNamespace(message=message)
            return types.SimpleNamespace(choices=[choice])

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            self.api_key = api_key
            self.chat = types.SimpleNamespace(
                completions=FakeCompletions(),
            )

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "Launch NISF for marketers who want better campaign copy.",
            "content_type": "marketing",
            "tone": "clear",
            "platform": "web",
            "variant_count": 2,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "groq"
    assert payload["model"] == "llama-3.3-70b-versatile"
    assert payload["variant_count"] == 2

    get_settings.cache_clear()


def test_generate_text_api_pads_groq_partial_response(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeCompletions:
        def create(self, **kwargs):
            message = types.SimpleNamespace(
                content='["Variant one with AI-powered smartphone.", "Variant two with smartphone.", "Variant three with mobile experience."]'
            )
            choice = types.SimpleNamespace(message=message)
            return types.SimpleNamespace(choices=[choice])

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            self.api_key = api_key
            self.chat = types.SimpleNamespace(completions=FakeCompletions())

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "Boost your mobile experience with our new AI-powered smartphone.",
            "brief": "Create a persuasive Instagram ad copy for young professionals in India.",
            "content_type": "ad_copy",
            "tone": "persuasive",
            "platform": "instagram",
            "variant_count": 5,
            "brand_terms": ["AI-powered", "smartphone", "mobile experience"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["variant_count"] == 5
    assert len(payload["variants"]) == 5
    assert [variant["id"] for variant in payload["variants"]] == ["v1", "v2", "v3", "v4", "v5"]
    assert len({variant["text"] for variant in payload["variants"]}) == 5

    get_settings.cache_clear()


def test_generate_text_api_truncates_groq_extra_response(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeCompletions:
        def create(self, **kwargs):
            message = types.SimpleNamespace(
                content='["One useful campaign line.", "Two useful campaign lines.", "Three useful campaign lines.", "Four useful campaign lines.", "Five useful campaign lines.", "Six useful campaign lines."]'
            )
            choice = types.SimpleNamespace(message=message)
            return types.SimpleNamespace(choices=[choice])

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            self.api_key = api_key
            self.chat = types.SimpleNamespace(completions=FakeCompletions())

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "Launch NISF for marketers who want better campaign copy.",
            "content_type": "marketing",
            "tone": "clear",
            "platform": "web",
            "variant_count": 3,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["variant_count"] == 3
    assert len(payload["variants"]) == 3
    assert [variant["id"] for variant in payload["variants"]] == ["v1", "v2", "v3"]

    get_settings.cache_clear()


def test_generate_text_api_reports_local_when_groq_generation_falls_back(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeCompletions:
        def create(self, **kwargs):
            raise RuntimeError("upstream failed")

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            self.api_key = api_key
            self.chat = types.SimpleNamespace(
                completions=FakeCompletions(),
            )

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_MODEL", "nisf-deterministic-local")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "Boost your mobile experience with our new AI-powered smartphone.",
            "brief": "Create a persuasive Instagram ad copy for young professionals in India.",
            "content_type": "ad_copy",
            "tone": "persuasive",
            "platform": "instagram",
            "variant_count": 2,
            "brand_terms": ["AI-powered", "smartphone", "mobile experience"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "local"
    assert payload["model"] == "nisf-deterministic-local"
    assert payload["variant_count"] == 2

    get_settings.cache_clear()


def test_generate_text_api_uses_local_provider_without_api_keys(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "local")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "Boost your mobile experience with our new AI-powered smartphone.",
            "brief": "Create a persuasive Instagram ad copy for young professionals in India.",
            "content_type": "ad_copy",
            "tone": "persuasive",
            "platform": "instagram",
            "variant_count": 5,
            "brand_terms": ["AI-powered", "smartphone", "mobile experience"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "local"
    assert payload["variant_count"] == 5
    assert len(payload["variants"]) == 5
    assert payload["variants"][0]["id"] == "v1"
    assert payload["variants"][0]["metadata"]["platform"] == "instagram"


def test_generate_text_api_uses_request_text_for_topic_specific_variants(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "local")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "Upgrade your daily routine with our smart fitness watch - track health, calls, and workouts in one stylish device.",
            "content_type": "marketing",
            "tone": "clear",
            "platform": "web",
            "variant_count": 3,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    joined = " ".join(variant["text"].lower() for variant in payload["variants"])
    assert payload["variant_count"] == 3
    assert len(payload["variants"]) == 3
    assert payload["variants"][0]["metadata"] == {
        "content_type": "marketing",
        "tone": "clear",
        "platform": "web",
    }
    assert "string" not in joined
    assert "less friction" not in joined
    assert sum(term in joined for term in ["smart", "fitness", "watch", "health", "calls", "workouts"]) >= 4


def test_generate_text_api_rejects_placeholder_text(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "local")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post(
        "/api/v1/generate/text",
        json={
            "text": "string",
            "content_type": "marketing",
            "tone": "clear",
            "platform": "web",
            "variant_count": 3,
        },
    )

    assert response.status_code == 422
    assert "real content" in response.text
