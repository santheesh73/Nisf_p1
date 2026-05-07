from app.utils.text_utils import clamp


class SafetyScorer:
    banned = {"hate", "violence", "kill", "scam", "fraud", "exploit"}

    def score(self, text: str, **kwargs) -> float:
        lowered = text.lower()
        penalty = sum(term in lowered for term in self.banned) * 35
        return clamp(100 - penalty)
