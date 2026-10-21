"""rename products brand column to category

Revision ID: a1b2c3d4e5f6
Revises: 7236e78bbcfd
Create Date: 2026-10-19 18:30:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '7236e78bbcfd'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('Products', schema='lyfter_ecommerce') as batch_op:
        batch_op.alter_column('brand', new_column_name='category')


def downgrade():
    with op.batch_alter_table('Products', schema='lyfter_ecommerce') as batch_op:
        batch_op.alter_column('category', new_column_name='brand')
