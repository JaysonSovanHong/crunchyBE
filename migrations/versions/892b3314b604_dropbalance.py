"""dropbalance

Revision ID: 892b3314b604
Revises: 1333202dc789
Create Date: 2021-05-24 12:19:45.310596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '892b3314b604'
down_revision = '1333202dc789'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users','balance')


def downgrade():
    pass
