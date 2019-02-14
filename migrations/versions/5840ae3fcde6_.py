"""empty message

Revision ID: 5840ae3fcde6
Revises: 45ec3f615902
Create Date: 2019-02-13 13:44:55.941240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5840ae3fcde6'
down_revision = '45ec3f615902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('activecompany', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'activecompany')
    # ### end Alembic commands ###