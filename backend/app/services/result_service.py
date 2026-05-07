"""
Result service — builds frontend-compatible result payloads from MongoDB
optimization job documents and persists pipeline output into the job.
"""

from app.db.mongo import OPTIMIZATION_JOBS, get_sync_collection
from app.schemas.critic_schema import CriticDirectiveSchema
from app.schemas.job_schema import JobResultResponse
from app.schemas.score_schema import ScoreBreakdown
from app.schemas.simulation_schema import SentimentResult, SimulationResultSchema
from app.schemas.variant_schema import VariantOut


class ResultService:
    """Reads/writes optimization results from/to the optimization_jobs collection."""

    def _collection(self):
        return get_sync_collection(OPTIMIZATION_JOBS)

    # --------------------------------------------------------------------- #
    # Persist pipeline output
    # --------------------------------------------------------------------- #

    def persist_result(self, job_id: str, result: dict) -> None:
        """Convert pipeline output into the nested MongoDB document shape and save."""
        variants_out: list[dict] = []
        best_variant_id: str | None = None
        content_type = result.get("content_type", "")
        tone = result.get("tone", "")
        platform = result.get("platform", "")

        for index, variant_out in enumerate(result["variants"], start=1):
            score_dict = variant_out.score.model_dump() if variant_out.score else None
            sim_dict = None
            if variant_out.simulation:
                sim_dict = {
                    "sentiment": {
                        "label": variant_out.simulation.sentiment.label,
                        "confidence": variant_out.simulation.sentiment.confidence,
                    },
                    "emotion": variant_out.simulation.emotions if hasattr(variant_out.simulation, "emotions") else {},
                }

            variant_id = variant_out.id if hasattr(variant_out, "id") and variant_out.id else f"v{index}"
            variant_doc = {
                "id": variant_id,
                "text": variant_out.content,
                "iteration": variant_out.iteration,
                "metadata": {
                    "content_type": content_type,
                    "tone": tone,
                    "platform": platform,
                    "provider": variant_out.source,
                },
                "scores": score_dict,
                "simulation": sim_dict,
                "is_best": False,
            }
            variants_out.append(variant_doc)

        # Determine best variant
        best = result.get("best_variant")
        directives_out: list[dict] = []
        scores_out = None

        if best:
            best_id = best.id if hasattr(best, "id") and best.id else variants_out[0]["id"]
            best_variant_id = best_id
            for v in variants_out:
                if v["id"] == best_id:
                    v["is_best"] = True
            if best.score:
                scores_out = best.score.model_dump()
            for d in best.critic_directives:
                directives_out.append(d.model_dump())

        update = {
            "variants": variants_out,
            "critic_directives": directives_out,
            "iteration_history": result["iteration_history"],
            "best_variant_id": best_variant_id,
            "scores": scores_out,
        }
        self._collection().update_one({"_id": job_id}, {"$set": update})

    # --------------------------------------------------------------------- #
    # Build frontend response
    # --------------------------------------------------------------------- #

    def build_job_result(self, job_doc: dict) -> JobResultResponse:
        """Convert a MongoDB job document into a ``JobResultResponse``."""
        directives = [
            CriticDirectiveSchema(**d) for d in job_doc.get("critic_directives", [])
        ]

        variants: list[VariantOut] = []
        best_variant_id = job_doc.get("best_variant_id")

        for v in job_doc.get("variants", []):
            score = None
            if v.get("scores"):
                score = ScoreBreakdown(**v["scores"])
            simulation = None
            sim_data = v.get("simulation")
            if sim_data and sim_data.get("sentiment"):
                simulation = SimulationResultSchema(
                    sentiment=SentimentResult(**sim_data["sentiment"]),
                    emotions=sim_data.get("emotion", {}),
                )
            variants.append(
                VariantOut(
                    id=v.get("id"),
                    iteration=v.get("iteration", 1),
                    content=v.get("text", ""),
                    source=v.get("metadata", {}).get("provider", "local"),
                    is_safe=True,
                    score=score,
                    simulation=simulation,
                    critic_directives=directives if v.get("id") == best_variant_id else [],
                )
            )

        best = next((v for v in variants if v.id == best_variant_id), None)
        if best is None and variants:
            best = max(
                variants,
                key=lambda variant: variant.score.attention_coefficient if variant.score else 0.0,
            )

        return JobResultResponse(
            job_id=job_doc["_id"],
            status=job_doc["status"],
            best_variant=best,
            variants=variants,
            scores=best.score if best else None,
            critic_directives=directives,
            iteration_history=job_doc.get("iteration_history", []),
            error=job_doc.get("error_message"),
        )
