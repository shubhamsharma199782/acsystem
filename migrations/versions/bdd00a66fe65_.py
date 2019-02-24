"""empty message

Revision ID: bdd00a66fe65
Revises: f9cc504ffdd7
Create Date: 2019-02-24 16:26:18.415123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdd00a66fe65'
down_revision = 'f9cc504ffdd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('booksbegin', sa.DateTime(), nullable=True))
    op.add_column('company', sa.Column('financialyear', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company', 'financialyear')
    op.drop_column('company', 'booksbegin')
    # ### end Alembic commands ###
