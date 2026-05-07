import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CriticDirective(Base):
    __tablename__ = "critic_directives"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(ForeignKey("optimization_jobs.id"), index=True)
    variant_id: Mapped[str | None] = mapped_column(ForeignKey("variants.id"), nullable=True)
    iteration: Mapped[int] = mapped_column(Integer, default=0)
    target_dimension: Mapped[str] = mapped_column(String(64))
    issue: Mapped[str] = mapped_column(Text)
    rewrite_instruction: Mapped[str] = mapped_column(Text)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    risk_level: Mapped[str] = mapped_column(String(32), default="low")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    job = relationship("OptimizationJob", back_populates="directives")
