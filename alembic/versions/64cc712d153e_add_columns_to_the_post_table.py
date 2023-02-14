"""add columns to the post table

Revision ID: 64cc712d153e
Revises: 0b2c53904cc4
Create Date: 2023-02-14 14:31:10.027444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64cc712d153e'
down_revision = '0b2c53904cc4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('post', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
