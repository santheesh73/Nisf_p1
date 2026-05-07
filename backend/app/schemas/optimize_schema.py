from pydantic import BaseModel, ConfigDict, Field, model_validator


class OptimizeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str | None = Field(default=None, max_length=12000)
    brief: str | None = Field(default=None, max_length=12000)
    content_type: str = "marketing"
    tone: str = "clear"
    platform: str = "web"
    max_iterations: int = Field(default=3, ge=1, le=5)
    target_score: float = Field(default=85.0, ge=0, le=100)
    convergence_threshold: float = Field(default=2.0, ge=0, le=100)
    variant_count: int = Field(default=4, ge=3, le=5)
    brand_terms: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_text_or_brief(self) -> "OptimizeRequest":
        if not (self.text or self.brief):
            raise ValueError("Either text or brief is required")
        return self


class OptimizeResponse(BaseModel):
    job_id: str
    status: str
