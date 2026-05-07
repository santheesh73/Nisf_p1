from app.utils.text_utils import clamp, words


class EngagementScorer:
    def score(self, text: str, **kwargs) -> float:
        tokens = words(text)
        power = {
            "capture",
            "discover",
            "finish",
            "faster",
            "productivity",
            "sharp",
            "sharper",
            "smooth",
            "smoother",
            "start",
            "build",
            "boost",
            "upgrade",
            "win",
            "unlock",
            "turn",
            "grow",
        }
        cta = {"click", "explore", "tap", "today", "upgrade", "start", "try", "discover", "learn", "join", "get", "build"}
        score = 45 + min(30, sum(t in power for t in tokens) * 6) + min(15, sum(t in cta for t in tokens) * 5)
        if "?" in text:
            score += 5
        if len(tokens) < 8:
            score -= 10
        return clamp(score)
