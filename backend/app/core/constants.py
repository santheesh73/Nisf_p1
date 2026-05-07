from enum import StrEnum


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    GENERATING = "generating"
    SIMULATING = "simulating"
    SCORING = "scoring"
    CRITICIZING = "criticizing"
    OPTIMIZING = "optimizing"
    SAFETY_CHECKING = "safety_checking"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Modality(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"


DEFAULT_SCORE_WEIGHTS = {
    "clarity": 0.20,
    "engagement": 0.25,
    "emotional_resonance": 0.20,
    "readability": 0.15,
    "originality": 0.10,
    "brand_fit": 0.05,
    "safety": 0.05,
}
