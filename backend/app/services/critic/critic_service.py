from app.providers.llm import get_llm_provider
from app.schemas.critic_schema import CriticDirectiveSchema
from app.schemas.score_schema import ScoreBreakdown
from app.services.critic.directive_builder import DirectiveBuilder


class CriticService:
    def __init__(self) -> None:
        self.provider = get_llm_provider()
        self.fallback = DirectiveBuilder()

    def critique(self, text: str, score: ScoreBreakdown) -> list[CriticDirectiveSchema]:
        scores = score.model_dump()
        try:
            directives = self.provider.generate_critic_feedback(text, scores)
            if directives:
                return directives
        except Exception:
            pass
        return self.fallback.build(scores)
