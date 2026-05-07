from collections.abc import Callable

from app.core.constants import JobStatus
from app.schemas.critic_schema import CriticDirectiveSchema
from app.schemas.optimize_schema import OptimizeRequest
from app.schemas.variant_schema import VariantOut
from app.services.critic import CriticService
from app.services.generation import GenerationService
from app.utils.text_quality import instagram_persuasive_quality_bonus, is_dirty_final_copy, polish_marketing_copy, quality_penalty
from app.services.optimization.best_variant_selector import BestVariantSelector
from app.services.optimization.convergence_detector import ConvergenceDetector
from app.services.safety import SafetyService
from app.services.scoring import ScoringService
from app.services.simulation import SimulationService

DEFAULT_CONVERGENCE_THRESHOLD = 2.0


class OptimizationController:
    def __init__(self) -> None:
        self.generation = GenerationService()
        self.simulation = SimulationService()
        self.scoring = ScoringService()
        self.critic = CriticService()
        self.safety = SafetyService()
        self.selector = BestVariantSelector()
        self.convergence = ConvergenceDetector()

    def optimize(self, request: OptimizeRequest, stage_callback: Callable[[JobStatus], None] | None = None) -> dict:
        all_variants: list[VariantOut] = []
        history: list[dict] = []
        directives: list[CriticDirectiveSchema] = []
        best_so_far: VariantOut | None = None
        previous_best = 0.0
        source_text = request.text
        source_brief = request.brief

        for iteration in range(request.max_iterations):
            if stage_callback:
                stage_callback(JobStatus.GENERATING)
            generated = self.generation.generate_variants(
                source_text,
                source_brief,
                request.content_type,
                request.tone,
                request.platform,
                request.variant_count,
                request.brand_terms,
                directives,
            )
            iteration_variants: list[VariantOut] = []
            for content in generated:
                variant_id = f"v{len(all_variants) + 1}"
                content = polish_marketing_copy(
                    content,
                    content_type=request.content_type,
                    tone=request.tone,
                    platform=request.platform,
                    brand_terms=request.brand_terms,
                )
                if stage_callback:
                    stage_callback(JobStatus.SAFETY_CHECKING)
                safety = self.safety.check_output(content)
                if stage_callback:
                    stage_callback(JobStatus.SIMULATING)
                simulation = self.simulation.simulate(content)
                if stage_callback:
                    stage_callback(JobStatus.SCORING)
                score = self.scoring.score_text(
                    content,
                    content_type=request.content_type,
                    tone=request.tone,
                    platform=request.platform,
                    emotions=simulation.emotions,
                    brand_terms=request.brand_terms,
                )
                variant = VariantOut(
                    id=variant_id,
                    iteration=iteration,
                    content=content,
                    source=self.generation.provider.name,
                    is_safe=safety["safe"]
                    and score.safety >= 70
                    and not is_dirty_final_copy(
                        content,
                        request.brand_terms,
                        request.content_type,
                        request.tone,
                        request.platform,
                    ),
                    score=score,
                    simulation=simulation,
                )
                iteration_variants.append(variant)
                all_variants.append(variant)

            iteration_best = self.selector.select(
                iteration_variants,
                request.brand_terms,
                request.content_type,
                request.tone,
                request.platform,
            )
            if iteration_best and (
                best_so_far is None
                or self._selection_score(iteration_best, request) > self._selection_score(best_so_far, request)
            ):
                best_so_far = iteration_best

            if best_so_far and best_so_far.score:
                final_content = polish_marketing_copy(
                    best_so_far.content,
                    content_type=request.content_type,
                    tone=request.tone,
                    platform=request.platform,
                    brand_terms=request.brand_terms,
                )
                final_score = self.scoring.score_text(
                    final_content,
                    content_type=request.content_type,
                    tone=request.tone,
                    platform=request.platform,
                    emotions=best_so_far.simulation.emotions if best_so_far.simulation else None,
                    brand_terms=request.brand_terms,
                )
                best_so_far.content = final_content
                best_so_far.score = final_score
                best_so_far.is_safe = best_so_far.is_safe and not is_dirty_final_copy(
                    final_content,
                    request.brand_terms,
                    request.content_type,
                    request.tone,
                    request.platform,
                )
                if not best_so_far.is_safe:
                    best_so_far = self.selector.select(
                        all_variants,
                        request.brand_terms,
                        request.content_type,
                        request.tone,
                        request.platform,
                    )

            best_score = best_so_far.score.attention_coefficient if best_so_far and best_so_far.score else 0.0
            improvement = best_score - previous_best
            stop_reason = None
            if best_score >= request.target_score:
                stop_reason = "target_score_reached"
            elif iteration > 0 and self.convergence.has_converged(improvement, request.convergence_threshold):
                stop_reason = "converged"

            if best_so_far and best_so_far.score:
                if stage_callback:
                    stage_callback(JobStatus.CRITICIZING)
                directives = self.critic.critique(best_so_far.content, best_so_far.score)
                best_so_far.critic_directives = directives

            history.append(
                {
                    "iteration": iteration,
                    "best_score": round(best_score, 2),
                    "improvement": round(improvement, 2),
                    "selected_variant": best_so_far.content if best_so_far else None,
                    "stop_reason": stop_reason,
                }
            )
            if stop_reason:
                break
            previous_best = best_score
            if best_so_far:
                source_text = best_so_far.content

        return {
            "best_variant": best_so_far,
            "variants": all_variants,
            "iteration_history": history,
            "content_type": request.content_type,
            "tone": request.tone,
            "platform": request.platform,
        }

    def _selection_score(self, variant: VariantOut, request: OptimizeRequest) -> float:
        if not variant.score:
            return 0.0
        return variant.score.attention_coefficient - quality_penalty(
            variant.content,
            request.brand_terms,
            request.content_type,
            request.tone,
            request.platform,
        ) + instagram_persuasive_quality_bonus(
            variant.content,
            request.brand_terms,
            request.content_type,
            request.tone,
            request.platform,
        )
