"""create index pub_date

Revision ID: 27762d1b22a5
Revises: f3f951d8cbdd
Create Date: 2023-01-16 01:39:52.498701

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '27762d1b22a5'
down_revision = 'f3f951d8cbdd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('index_pub_date', 'post', ['pub_date'])
    op.create_index('index_mode', 'post', ['mode'])


def downgrade():
    op.drop_index('index_pub_date', 'post')
    op.drop_index('index_mode', 'mode')
