"""add class table

Revision ID: fd454efbe266
Revises: 1dfc89ae4858
Create Date: 2023-02-14 14:23:19.742996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd454efbe266'
down_revision = '1dfc89ae4858'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('class_info',
                    sa.Column('class_name', sa.String(), nullable=False),
                    sa.Column('teacher', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('class_name')
                    )
    pass


def downgrade():
    op.drop_table("class_info")
    pass
