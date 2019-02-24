"""empty message

Revision ID: c3a446845a56
Revises: fd5a7ad86143
Create Date: 2019-02-24 17:05:47.811310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3a446845a56'
down_revision = 'fd5a7ad86143'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('currentbalance', sa.Integer(), nullable=True))
    op.add_column('customer', sa.Column('openingbalance', sa.Integer(), nullable=True))
    op.add_column('supplier', sa.Column('currentbalance', sa.Integer(), nullable=True))
    op.add_column('supplier', sa.Column('openingbalance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('supplier', 'openingbalance')
    op.drop_column('supplier', 'currentbalance')
    op.drop_column('customer', 'openingbalance')
    op.drop_column('customer', 'currentbalance')
    # ### end Alembic commands ###
