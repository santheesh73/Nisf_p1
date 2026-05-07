import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import JobStatus
from app.db.base import Base


class OptimizationJob(Base):
    __tablename__ = "optimization_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status: Mapped[str] = mapped_column(String(32), default=JobStatus.QUEUED.value, index=True)
    input_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    brief: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(64), default="marketing")
    tone: Mapped[str] = mapped_column(String(64), default="clear")
    platform: Mapped[str] = mapped_column(String(64), default="web")
    max_iterations: Mapped[int] = mapped_column(Integer, default=3)
    target_score: Mapped[float] = mapped_column(Float, default=85.0)
    variant_count: Mapped[int] = mapped_column(Integer, default=4)
    brand_terms: Mapped[list] = mapped_column(JSON, default=list)
    best_variant_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    iteration_history: Mapped[list] = mapped_column(JSON, default=list)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    variants = relationship("Variant", back_populates="job", cascade="all, delete-orphan")
    directives = relationship("CriticDirective", back_populates="job", cascade="all, delete-orphan")
