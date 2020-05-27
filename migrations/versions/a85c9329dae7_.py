"""empty message

Revision ID: a85c9329dae7
Revises: e41dafbb7468
Create Date: 2020-03-13 12:52:53.690329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a85c9329dae7'
down_revision = 'e41dafbb7468'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('artists', sa.Column('seeking_description', sa.String(), nullable=True))
    op.add_column('artists', sa.Column('website', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'website')
    op.drop_column('artists', 'seeking_description')
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###
