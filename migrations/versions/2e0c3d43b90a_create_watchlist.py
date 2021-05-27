"""create-watchlist

Revision ID: 2e0c3d43b90a
Revises: 1333202dc789
Create Date: 2021-05-27 10:51:08.604998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0c3d43b90a'
down_revision = '1333202dc789'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'watchlist',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('crypto_id', sa.Integer),
    sa.Column('name', sa.String)
  )


def downgrade():
    op.drop_table('watchlist')


# user.cryptos.append(crypto)