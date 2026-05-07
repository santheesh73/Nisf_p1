"""frontend contract fields

Revision ID: 0002_frontend_contract_fields
Revises: 0001_initial
Create Date: 2026-05-05
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_frontend_contract_fields"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("optimization_jobs", sa.Column("variant_count", sa.Integer(), nullable=True))
    op.add_column("optimization_jobs", sa.Column("brand_terms", sa.JSON(), nullable=True))
    op.add_column("feedback_metrics", sa.Column("platform", sa.String(64), nullable=True))


def downgrade() -> None:
    op.drop_column("feedback_metrics", "platform")
    op.drop_column("optimization_jobs", "brand_terms")
    op.drop_column("optimization_jobs", "variant_count")
