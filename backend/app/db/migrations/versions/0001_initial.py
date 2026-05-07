"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-30
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "optimization_jobs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("status", sa.String(32), index=True),
        sa.Column("input_text", sa.Text(), nullable=True),
        sa.Column("brief", sa.Text(), nullable=True),
        sa.Column("content_type", sa.String(64)),
        sa.Column("tone", sa.String(64)),
        sa.Column("platform", sa.String(64)),
        sa.Column("max_iterations", sa.Integer()),
        sa.Column("target_score", sa.Float()),
        sa.Column("best_variant_id", sa.String(36), nullable=True),
        sa.Column("iteration_history", sa.JSON()),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )
    op.create_table(
        "variants",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("job_id", sa.String(36), sa.ForeignKey("optimization_jobs.id"), index=True),
        sa.Column("iteration", sa.Integer()),
        sa.Column("content", sa.Text()),
        sa.Column("source", sa.String(64)),
        sa.Column("is_safe", sa.Boolean()),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "variant_scores",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("variant_id", sa.String(36), sa.ForeignKey("variants.id"), unique=True, index=True),
        sa.Column("clarity", sa.Float()),
        sa.Column("engagement", sa.Float()),
        sa.Column("emotional_resonance", sa.Float()),
        sa.Column("readability", sa.Float()),
        sa.Column("originality", sa.Float()),
        sa.Column("brand_fit", sa.Float()),
        sa.Column("safety", sa.Float()),
        sa.Column("attention_coefficient", sa.Float()),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "simulation_results",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("variant_id", sa.String(36), sa.ForeignKey("variants.id"), index=True),
        sa.Column("sentiment_label", sa.String(32)),
        sa.Column("sentiment_confidence", sa.Float()),
        sa.Column("emotions", sa.JSON()),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "critic_directives",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("job_id", sa.String(36), sa.ForeignKey("optimization_jobs.id"), index=True),
        sa.Column("variant_id", sa.String(36), sa.ForeignKey("variants.id"), nullable=True),
        sa.Column("iteration", sa.Integer()),
        sa.Column("target_dimension", sa.String(64)),
        sa.Column("issue", sa.Text()),
        sa.Column("rewrite_instruction", sa.Text()),
        sa.Column("priority", sa.Integer()),
        sa.Column("risk_level", sa.String(32)),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(120), unique=True),
        sa.Column("content_type", sa.String(64)),
        sa.Column("description", sa.Text()),
        sa.Column("prompt_pattern", sa.Text()),
        sa.Column("is_active", sa.Boolean()),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "feedback_metrics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("job_id", sa.String(36), index=True, nullable=True),
        sa.Column("variant_id", sa.String(36), index=True, nullable=True),
        sa.Column("impressions", sa.Integer()),
        sa.Column("clicks", sa.Integer()),
        sa.Column("likes", sa.Integer()),
        sa.Column("shares", sa.Integer()),
        sa.Column("conversions", sa.Integer()),
        sa.Column("ctr", sa.Float()),
        sa.Column("conversion_rate", sa.Float()),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_table(
        "model_registry",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider", sa.String(64)),
        sa.Column("model_name", sa.String(255)),
        sa.Column("modality", sa.String(32)),
        sa.Column("capabilities", sa.JSON()),
        sa.Column("is_active", sa.Boolean()),
        sa.Column("created_at", sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table("model_registry")
    op.drop_table("feedback_metrics")
    op.drop_table("templates")
    op.drop_table("critic_directives")
    op.drop_table("simulation_results")
    op.drop_table("variant_scores")
    op.drop_table("variants")
    op.drop_table("optimization_jobs")
