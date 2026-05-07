from app.schemas.variant_schema import VariantOut
from app.utils.text_quality import instagram_persuasive_quality_bonus, passes_minimum_naturalness, quality_penalty


class BestVariantSelector:
    def select(
        self,
        variants: list[VariantOut],
        brand_terms: list[str] | None = None,
        content_type: str = "marketing",
        tone: str = "clear",
        platform: str = "web",
    ) -> VariantOut | None:
        safe = [
            variant
            for variant in variants
            if variant.is_safe
            and variant.score
            and passes_minimum_naturalness(variant.content, brand_terms, content_type, tone, platform)
        ]
        if not safe:
            return None
        return max(
            safe,
            key=lambda variant: variant.score.attention_coefficient
            + instagram_persuasive_quality_bonus(variant.content, brand_terms, content_type, tone, platform)
            - quality_penalty(variant.content, brand_terms, content_type, tone, platform),
        )
