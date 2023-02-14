"""add foreign key to post table

Revision ID: 0b2c53904cc4
Revises: fd454efbe266
Create Date: 2023-02-14 14:26:21.956819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b2c53904cc4'
down_revision = 'fd454efbe266'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("post", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key('post_users_fk', source_table="post", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="post")
    op.drop_column("post", "owner_id")
    pass
