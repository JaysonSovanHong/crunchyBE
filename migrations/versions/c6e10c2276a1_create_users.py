"""create-users

Revision ID: c6e10c2276a1
Revises: 
Create Date: 2021-05-21 16:08:05.967026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6e10c2276a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'users',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
    
  )


def downgrade():
    op.drop_table('users')
