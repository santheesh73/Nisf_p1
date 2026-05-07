from app.utils.text_utils import clamp


class BrandFitScorer:
    def score(self, text: str, tone: str = "clear", brand_terms: list[str] | None = None, **kwargs) -> float:
        lowered = text.lower()
        score = 65
        if tone and tone.lower() in lowered:
            score += 8
        if brand_terms:
            hits = sum(term.lower() in lowered for term in brand_terms)
            score += min(22, hits * 7)
        else:
            score += 10
        return clamp(score)
