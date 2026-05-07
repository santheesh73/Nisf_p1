import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VariantScore(Base):
    __tablename__ = "variant_scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variant_id: Mapped[str] = mapped_column(ForeignKey("variants.id"), unique=True, index=True)
    clarity: Mapped[float] = mapped_column(Float)
    engagement: Mapped[float] = mapped_column(Float)
    emotional_resonance: Mapped[float] = mapped_column(Float)
    readability: Mapped[float] = mapped_column(Float)
    originality: Mapped[float] = mapped_column(Float)
    brand_fit: Mapped[float] = mapped_column(Float)
    safety: Mapped[float] = mapped_column(Float)
    attention_coefficient: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    variant = relationship("Variant", back_populates="score")
