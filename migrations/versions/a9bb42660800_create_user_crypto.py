"""create-user_crypto

Revision ID: a9bb42660800
Revises: c6e10c2276a1
Create Date: 2021-05-21 16:08:55.236717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9bb42660800'
down_revision = 'c6e10c2276a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_crypto',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id',sa.Integer),
        sa.Column('crypto_id',sa.Integer),
        sa.Column('amount',sa.Integer)
    )


def downgrade():
    op.drop_table('user_crypto')
