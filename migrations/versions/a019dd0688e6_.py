"""empty message

Revision ID: a019dd0688e6
Revises: 2c9aed459513
Create Date: 2020-03-31 10:33:02.555353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a019dd0688e6'
down_revision = '2c9aed459513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('artists', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('venues', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('shows', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('artists', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artists', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.alter_column('artists', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
