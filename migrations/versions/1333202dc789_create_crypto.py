"""create-crypto

Revision ID: 1333202dc789
Revises: c6e10c2276a1
Create Date: 2021-05-21 16:09:02.695816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1333202dc789'
down_revision = 'c6e10c2276a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'crypto',
        sa.Column('id',sa.INTEGER, primary_key=True),
        sa.Column('crypto_code',sa.String),

    )


def downgrade():
    op.drop_table('crypto')
