"""allow guest orders without user or cart

Revision ID: c8d9e0f1a2b3
Revises: b7c8d9e0f1a2
Create Date: 2026-11-16 17:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "c8d9e0f1a2b3"
down_revision = "b7c8d9e0f1a2"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("Orders", schema="lyfter_ecommerce") as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("cart_id", existing_type=sa.Integer(), nullable=True)


def downgrade():
    with op.batch_alter_table("Orders", schema="lyfter_ecommerce") as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("cart_id", existing_type=sa.Integer(), nullable=False)
