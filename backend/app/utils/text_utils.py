import re


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def sentence_count(text: str) -> int:
    return max(1, len(re.findall(r"[.!?]+", text)) or 1)


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return round(max(minimum, min(maximum, value)), 2)
