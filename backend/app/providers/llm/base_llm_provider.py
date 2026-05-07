from abc import ABC, abstractmethod

from app.schemas.critic_schema import CriticDirectiveSchema


class BaseLLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def generate_variants(
        self,
        source_text: str,
        content_type: str,
        tone: str,
        platform: str,
        count: int,
        brand_terms: list[str] | None = None,
        directives: list[CriticDirectiveSchema] | None = None,
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def generate_critic_feedback(self, text: str, scores: dict[str, float]) -> list[CriticDirectiveSchema]:
        raise NotImplementedError
