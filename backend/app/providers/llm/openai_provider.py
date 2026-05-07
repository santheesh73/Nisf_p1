from app.providers.llm.local_provider import LocalLLMProvider


class OpenAIProvider(LocalLLMProvider):
    name = "openai"
