import sys
import types

from app.core.config import ENV_FILE, get_settings
from app.providers.llm import get_llm_provider
from app.providers.llm.groq_provider import GroqProvider
from app.providers.llm.local_provider import LocalLLMProvider


def test_settings_loads_env_from_backend_root():
    assert ENV_FILE.name == ".env"
    assert ENV_FILE.parent.name == "backend"


def test_groq_provider_selected_when_env_has_provider_and_key(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            self.api_key = api_key

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, GroqProvider)
    assert provider.name == "groq"
    assert provider.model == "llama-3.3-70b-versatile"

    get_settings.cache_clear()


def test_groq_provider_falls_back_to_local_without_key(monkeypatch, caplog):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, LocalLLMProvider)
    assert "Groq API key missing. Falling back to local provider." in caplog.text
    assert "test-key" not in caplog.text

    get_settings.cache_clear()


def test_groq_provider_fails_without_key_when_fallback_disabled(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "")
    monkeypatch.setenv("ALLOW_LLM_FALLBACK", "false")
    get_settings.cache_clear()

    try:
        try:
            get_llm_provider()
            assert False, "Expected missing-key configuration to fail when fallback is disabled."
        except RuntimeError as exc:
            assert "fallback is disabled" in str(exc).lower()
    finally:
        get_settings.cache_clear()


def test_groq_provider_falls_back_to_local_when_initialization_fails(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            raise RuntimeError("sdk construction failed")

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, LocalLLMProvider)

    get_settings.cache_clear()


def test_groq_provider_fails_when_initialization_breaks_and_fallback_disabled(monkeypatch):
    fake_groq_module = types.ModuleType("groq")

    class FakeGroq:
        def __init__(self, api_key, timeout=None):
            raise RuntimeError("sdk construction failed")

    fake_groq_module.Groq = FakeGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("ALLOW_LLM_FALLBACK", "false")
    get_settings.cache_clear()

    try:
        try:
            get_llm_provider()
            assert False, "Expected initialization failure when fallback is disabled."
        except RuntimeError as exc:
            assert "fallback is disabled" in str(exc).lower()
    finally:
        get_settings.cache_clear()
