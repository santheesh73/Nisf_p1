from app.providers.llm.local_provider import LocalLLMProvider


class GeminiProvider(LocalLLMProvider):
    name = "gemini"
