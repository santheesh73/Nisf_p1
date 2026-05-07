from app.schemas.score_schema import ScoreBreakdown
from app.services.scoring.brand_fit_scorer import BrandFitScorer
from app.services.scoring.clarity_scorer import ClarityScorer
from app.services.scoring.composite_scorer import CompositeScorer
from app.services.scoring.emotion_scorer import EmotionScorer
from app.services.scoring.engagement_scorer import EngagementScorer
from app.services.scoring.originality_scorer import OriginalityScorer
from app.services.scoring.readability_scorer import ReadabilityScorer
from app.services.scoring.safety_scorer import SafetyScorer
from app.utils.text_quality import quality_penalty
from app.utils.text_utils import clamp


class ScoringService:
    def __init__(self) -> None:
        self.clarity = ClarityScorer()
        self.engagement = EngagementScorer()
        self.emotion = EmotionScorer()
        self.readability = ReadabilityScorer()
        self.originality = OriginalityScorer()
        self.brand_fit = BrandFitScorer()
        self.safety = SafetyScorer()
        self.composite = CompositeScorer()

    def score_text(
        self,
        text: str,
        content_type: str = "marketing",
        tone: str = "clear",
        platform: str = "web",
        emotions: dict[str, float] | None = None,
        brand_terms: list[str] | None = None,
    ) -> ScoreBreakdown:
        dimensions = {
            "clarity": self.clarity.score(text),
            "engagement": self.engagement.score(text),
            "emotional_resonance": self.emotion.score(text, emotions=emotions),
            "readability": self.readability.score(text),
            "originality": self.originality.score(text),
            "brand_fit": self.brand_fit.score(text, tone=tone, brand_terms=brand_terms),
            "safety": self.safety.score(text),
        }
        penalty = quality_penalty(
            text,
            brand_terms=brand_terms,
            content_type=content_type,
            tone=tone,
            platform=platform,
        )
        if penalty:
            dimensions = {key: clamp(value - penalty) for key, value in dimensions.items()}
        return self.composite.score(dimensions)
