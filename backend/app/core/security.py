from app.services.safety.prompt_injection_filter import PromptInjectionFilter


def sanitize_prompt_input(text: str) -> str:
    return PromptInjectionFilter().sanitize(text)
