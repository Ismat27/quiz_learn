"""empty message

Revision ID: ba79887d9e4a
Revises: 3012ceb36fbc
Create Date: 2022-10-05 11:38:14.252958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba79887d9e4a'
down_revision = '3012ceb36fbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leaderboard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('cap', sa.Integer(), nullable=False),
    sa.Column('cp', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leaderboard')
    # ### end Alembic commands ###
