class UsageService:
    def record_usage(self, provider: str, model: str | None = None, units: int = 1) -> dict:
        return {"provider": provider, "model": model, "units": units}
