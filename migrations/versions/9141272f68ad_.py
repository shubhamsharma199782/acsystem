"""empty message

Revision ID: 9141272f68ad
Revises: c9b57c741c81
Create Date: 2019-04-16 00:30:42.879019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9141272f68ad'
down_revision = 'c9b57c741c81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sales', sa.Column('description', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sales', 'description')
    # ### end Alembic commands ###
