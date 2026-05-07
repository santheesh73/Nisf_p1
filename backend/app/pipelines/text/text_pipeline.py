from app.core.exceptions import NISFError
from app.pipelines.base_pipeline import BasePipeline
from app.schemas.optimize_schema import OptimizeRequest
from app.services.critic import CriticService
from app.services.generation import GenerationService
from app.services.optimization import OptimizationController
from app.services.scoring import ScoringService
from app.services.simulation import SimulationService


class TextPipeline(BasePipeline):
    def __init__(self) -> None:
        self.controller = OptimizationController()
        self.generation_service = GenerationService()
        self.simulation_service = SimulationService()
        self.scoring_service = ScoringService()
        self.critic_service = CriticService()

    def validate_input(self, payload: OptimizeRequest) -> None:
        if not (payload.text or payload.brief):
            raise NISFError("Either text or brief is required")

    def generate(self, payload: OptimizeRequest):
        return self.generation_service.generate_variants(
            payload.text,
            payload.brief,
            payload.content_type,
            payload.tone,
            payload.platform,
            payload.variant_count,
            payload.brand_terms,
        )

    def simulate(self, payload: str):
        return self.simulation_service.simulate(payload)

    def score(self, payload: str):
        return self.scoring_service.score_text(payload)

    def critique(self, payload):
        text, score = payload
        return self.critic_service.critique(text, score)

    def optimize(self, payload: OptimizeRequest, stage_callback=None) -> dict:
        self.validate_input(payload)
        return self.controller.optimize(payload, stage_callback=stage_callback)

    def build_output(self, payload: dict) -> dict:
        return payload
