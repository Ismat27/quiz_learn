"""empty message

Revision ID: 2d4d9909f5d9
Revises: b6551368644f
Create Date: 2023-01-08 11:26:33.017698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d4d9909f5d9'
down_revision = 'b6551368644f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spins')
    # ### end Alembic commands ###
