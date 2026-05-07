class PromptInjectionFilter:
    suspicious = [
        "ignore previous instructions",
        "system prompt",
        "developer message",
        "reveal hidden",
        "bypass safety",
    ]

    def is_suspicious(self, text: str) -> bool:
        lowered = text.lower()
        return any(pattern in lowered for pattern in self.suspicious)

    def sanitize(self, text: str) -> str:
        cleaned = text
        for pattern in self.suspicious:
            cleaned = cleaned.replace(pattern, "[filtered]")
            cleaned = cleaned.replace(pattern.title(), "[filtered]")
        return cleaned.strip()
