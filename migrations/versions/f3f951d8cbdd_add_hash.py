"""Add hash

Revision ID: f3f951d8cbdd
Revises: 207c8ed632a2
Create Date: 2023-01-16 01:11:41.790981

"""
from alembic import op
from sqlalchemy import INTEGER, VARCHAR, Column, ForeignKey, BOOLEAN, TEXT, DATETIME


# revision identifiers, used by Alembic.
revision = 'f3f951d8cbdd'
down_revision = '207c8ed632a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('post','_post')
    op.create_table('post',
                    Column('id', INTEGER, primary_key=True),
                    Column('ovner', INTEGER, ForeignKey('user.id'), nullable=False),
                    Column('forward', BOOLEAN, unique=False, default=False, nullable=False),
                    Column('title', VARCHAR(256), default='', nullable=False),
                    Column('pub_date', DATETIME, default='CURRENT_TIMESTAMP'),
                    Column('last_modified', DATETIME, default='CURRENT_TIMESTAMP'),
                    Column('sity', VARCHAR(80), default='', nullable=False),
                    Column('content', TEXT, default='', nullable=False),
                    Column('typograf', TEXT, default='', nullable=False),
                    Column('hash', VARCHAR(40), default='', nullable=False),
                    Column('pub', BOOLEAN, unique=False, default=False, nullable=False),
                    Column('mode', VARCHAR(80), default='', nullable=False),
                    )
    op.execute('INSERT INTO post SELECT `id`,`ovner`,`forward`,`title`,`pub_date`,`last_modified`,`sity`,`content`,`typograf`,"",0,"" FROM _post')
    op.drop_table('_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'hash')
    op.drop_column('post', 'pub')
    # ### end Alembic commands ###
