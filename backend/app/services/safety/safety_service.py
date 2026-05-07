from app.services.safety.content_moderation import ContentModeration
from app.services.safety.prompt_injection_filter import PromptInjectionFilter


class SafetyService:
    def __init__(self) -> None:
        self.injection = PromptInjectionFilter()
        self.moderation = ContentModeration()

    def sanitize_input(self, text: str) -> str:
        return self.injection.sanitize(text)

    def check_output(self, text: str) -> dict:
        moderation = self.moderation.check(text)
        return {
            "safe": moderation["safe"] and not self.injection.is_suspicious(text),
            "flags": moderation["flags"],
            "prompt_injection": self.injection.is_suspicious(text),
        }
