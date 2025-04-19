"""Drop and recreate prediction_log with non-nullable fields

Revision ID: 9d761dc4b8ad
Revises:
Create Date: 2025-04-17 10:53:19.469964

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9d761dc4b8ad"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop the old table
    op.drop_table("prediction_log")

    # Recreate with updated schema
    op.create_table(
        "prediction_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("ip_address", sa.String(length=100)),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("tenor", sa.Integer(), nullable=False),
        sa.Column("predicted_price", sa.Float(), nullable=False),
        sa.Column("predicted_buyback", sa.Float(), nullable=False),
        sa.Column("gold_gram", sa.Float(), nullable=False),
        sa.Column("profit_gold", sa.Float(), nullable=False),
        sa.Column("profit_deposit", sa.Float(), nullable=False),
        sa.Column("gold_return_rate", sa.Float(), nullable=False),
        sa.Column("deposit_return_rate", sa.Float(), nullable=False),
        sa.Column("recommendation", sa.String(length=10), nullable=False),
    )


def downgrade():
    op.drop_table("prediction_log")
