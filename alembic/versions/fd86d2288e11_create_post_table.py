"""Create post table

Revision ID: fd86d2288e11
Revises: 
Create Date: 2023-02-14 14:05:09.457787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd86d2288e11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("post", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
