from app.providers.llm.local_provider import LocalLLMProvider


class HuggingFaceProvider(LocalLLMProvider):
    name = "huggingface"
