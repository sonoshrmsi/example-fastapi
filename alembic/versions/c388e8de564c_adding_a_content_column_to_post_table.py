"""Adding a content column to post table

Revision ID: c388e8de564c
Revises: fd86d2288e11
Create Date: 2023-02-14 14:14:55.739961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c388e8de564c'
down_revision = 'fd86d2288e11'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("post", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("post", "content")
    pass
