from app.schemas.critic_schema import CriticDirectiveSchema


class DirectiveBuilder:
    REWRITE_GUIDANCE = {
        "readability": "Shorten sentences, simplify words, remove filler, and improve punctuation.",
        "engagement": "Strengthen the hook, make the first benefit more immediate, and use a clearer CTA.",
        "brand_fit": "Use brand terms naturally so the copy feels specific and on-brand.",
        "clarity": "State the product and benefit more directly with concrete wording.",
        "emotional_resonance": "Connect the benefit to speed, confidence, ease, creativity, or control.",
        "originality": "Replace generic claims with specific, distinctive outcomes.",
        "safety": "Keep the copy appropriate, accurate, and free of risky wording.",
    }

    def build(self, scores: dict[str, float]) -> list[CriticDirectiveSchema]:
        directives: list[CriticDirectiveSchema] = []
        for priority, (dimension, score) in enumerate(sorted(scores.items(), key=lambda item: item[1]), start=1):
            if dimension == "attention_coefficient" or priority > 3:
                continue
            directives.append(
                CriticDirectiveSchema(
                    target_dimension=dimension,
                    issue=f"{dimension.replace('_', ' ').title()} scored {score:.1f}, below the optimization target.",
                    rewrite_instruction=self.REWRITE_GUIDANCE.get(
                        dimension,
                        f"Raise {dimension.replace('_', ' ')} with specific, concise marketing language.",
                    ),
                    priority=priority,
                    risk_level="high" if score < 45 else "medium" if score < 65 else "low",
                )
            )
        return directives
