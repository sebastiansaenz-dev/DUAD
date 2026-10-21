"""add Categories table and product category_id FK

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f6
Create Date: 2026-10-19 18:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7c8d9e0f1a2'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        schema='lyfter_ecommerce'
    )

    op.execute(
        '''
        INSERT INTO lyfter_ecommerce."Categories" (name)
        SELECT DISTINCT category
        FROM lyfter_ecommerce."Products"
        WHERE category IS NOT NULL
        '''
    )

    with op.batch_alter_table('Products', schema='lyfter_ecommerce') as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))

    op.execute(
        '''
        UPDATE lyfter_ecommerce."Products" AS products
        SET category_id = categories.id
        FROM lyfter_ecommerce."Categories" AS categories
        WHERE products.category = categories.name
        '''
    )

    with op.batch_alter_table('Products', schema='lyfter_ecommerce') as batch_op:
        batch_op.alter_column('category_id', existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key(
            'fk_products_category_id',
            'Categories',
            ['category_id'],
            ['id'],
            referent_schema='lyfter_ecommerce'
        )
        batch_op.drop_column('category')


def downgrade():
    with op.batch_alter_table('Products', schema='lyfter_ecommerce') as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(), nullable=True))

    op.execute(
        '''
        UPDATE lyfter_ecommerce."Products" AS products
        SET category = categories.name
        FROM lyfter_ecommerce."Categories" AS categories
        WHERE products.category_id = categories.id
        '''
    )

    with op.batch_alter_table('Products', schema='lyfter_ecommerce') as batch_op:
        batch_op.alter_column('category', existing_type=sa.String(), nullable=False)
        batch_op.drop_constraint('fk_products_category_id', type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('Categories', schema='lyfter_ecommerce')
