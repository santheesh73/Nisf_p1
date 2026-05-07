import logging

from app.core.config import get_settings
from app.providers.llm.base_llm_provider import BaseLLMProvider
from app.providers.llm.gemini_provider import GeminiProvider
from app.providers.llm.groq_provider import GroqProvider
from app.providers.llm.huggingface_provider import HuggingFaceProvider
from app.providers.llm.local_provider import LocalLLMProvider
from app.providers.llm.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


def get_llm_provider() -> BaseLLMProvider:
    settings = get_settings()
    provider = settings.llm_provider.strip().lower()
    if provider == "local":
        logger.info("llm_provider_selected", extra={"provider": "local", "reason": "LLM_PROVIDER is local"})
        return LocalLLMProvider()
    if provider == "groq":
        if settings.groq_api_key:
            try:
                selected = GroqProvider(api_key=settings.groq_api_key, model=settings.groq_model)
            except Exception as exc:
                if not settings.allow_llm_fallback:
                    raise RuntimeError("Groq initialization failed and local fallback is disabled.") from exc
                logger.warning(
                    "llm_provider_falling_back_to_local",
                    extra={
                        "requested_provider": "groq",
                        "reason": "Groq initialization failed",
                        "error": str(exc),
                    },
                )
                return LocalLLMProvider()
            logger.info("llm_provider_selected", extra={"provider": "groq", "model": selected.model})
            return selected
        if not settings.allow_llm_fallback:
            raise RuntimeError("GROQ_API_KEY is missing and local fallback is disabled.")
        logger.warning(
            "Groq API key missing. Falling back to local provider.",
            extra={"requested_provider": "groq", "reason": "GROQ_API_KEY is missing"},
        )
        return LocalLLMProvider()
    if provider == "openai" and settings.openai_api_key:
        return OpenAIProvider()
    if provider == "gemini" and settings.gemini_api_key:
        return GeminiProvider()
    if provider == "huggingface" and settings.huggingface_api_key:
        return HuggingFaceProvider()
    return LocalLLMProvider()
