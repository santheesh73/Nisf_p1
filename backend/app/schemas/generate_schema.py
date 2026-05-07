from pydantic import BaseModel, ConfigDict, Field, model_validator


PLACEHOLDER_VALUES = {
    "string",
    "text",
    "sample",
    "example",
    "placeholder",
    "your text",
    "enter text",
    "lorem ipsum",
}


class GenerateTextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str | None = Field(default=None, max_length=12000)
    brief: str | None = Field(default=None, max_length=12000)
    content_type: str = "marketing"
    tone: str = "clear"
    platform: str = "web"
    variant_count: int = Field(default=3, ge=1, le=5)
    brand_terms: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_text_or_brief(self) -> "GenerateTextRequest":
        self.text = self._normalize_optional_text(self.text)
        self.brief = self._normalize_optional_text(self.brief)
        if not (self.text or self.brief):
            raise ValueError("Either text or brief is required")
        if self.text is not None:
            self._reject_placeholder(self.text, "text")
        if self.brief is not None:
            self._reject_placeholder(self.brief, "brief")
        return self

    @staticmethod
    def _normalize_optional_text(value: str | None) -> str | None:
        if value is None:
            return None
        normalized = " ".join(value.split())
        return normalized or None

    @staticmethod
    def _reject_placeholder(value: str, field_name: str) -> None:
        normalized = value.strip().lower()
        if normalized in PLACEHOLDER_VALUES:
            raise ValueError(f"{field_name} must contain real content, not placeholder text")


class GenerateVariant(BaseModel):
    id: str
    text: str
    metadata: dict[str, str]


class GenerateTextResponse(BaseModel):
    provider: str
    model: str
    variant_count: int
    variants: list[GenerateVariant]
