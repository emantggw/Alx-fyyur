"""empty message

Revision ID: 49bd3f41a36d
Revises: bc06e8bf4eb7
Create Date: 2022-08-15 17:31:25.749607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49bd3f41a36d'
down_revision = 'bc06e8bf4eb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'upcoming_shows_count')
    op.drop_column('artist', 'past_shows_count')
    op.drop_column('shows', 'upcoming')
    op.drop_column('venue', 'upcoming_shows_count')
    op.drop_column('venue', 'past_shows_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('venue', sa.Column('upcoming_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('shows', sa.Column('upcoming', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('artist', sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('upcoming_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
