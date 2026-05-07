from app.utils.text_utils import clamp, words


class OriginalityScorer:
    def score(self, text: str, **kwargs) -> float:
        tokens = words(text)
        if not tokens:
            return 0
        unique_ratio = len(set(tokens)) / len(tokens)
        cliche_penalty = sum(phrase in text.lower() for phrase in ["game changer", "best in class", "next level"]) * 8
        return clamp(45 + unique_ratio * 55 - cliche_penalty)
