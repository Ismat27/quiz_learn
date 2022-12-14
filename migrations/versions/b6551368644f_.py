"""empty message

Revision ID: b6551368644f
Revises: 
Create Date: 2022-11-25 06:29:59.404798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6551368644f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('access_points', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quiz_questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('option_a', sa.Text(), nullable=False),
    sa.Column('option_b', sa.Text(), nullable=False),
    sa.Column('option_c', sa.Text(), nullable=False),
    sa.Column('option_d', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('cp_wrong', sa.Integer(), nullable=False),
    sa.Column('cp_right', sa.Integer(), nullable=False),
    sa.Column('cap_wrong', sa.Integer(), nullable=False),
    sa.Column('cap_right', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('username', sa.String(length=200), server_default='unknown', nullable=True),
    sa.Column('first_name', sa.String(length=200), nullable=True),
    sa.Column('last_name', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('is_superuser', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('signup_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_seen', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('cp', sa.Integer(), server_default='0', nullable=False),
    sa.Column('cap', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leaderboard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('cap', sa.Integer(), nullable=False),
    sa.Column('cp', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quiz_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('questions', sa.Text(), nullable=True),
    sa.Column('score', sa.Integer(), server_default='0', nullable=True),
    sa.Column('completed', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referrals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('commission', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('status', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('refered_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['refered_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_wallets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('balance', sa.Numeric(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('transaction_type', sa.String(length=50), server_default='subscription', nullable=False),
    sa.Column('status', sa.String(length=50), server_default='pending', nullable=False),
    sa.Column('paystack_reference', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['wallet_id'], ['user_wallets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_transactions')
    op.drop_table('user_wallets')
    op.drop_table('referrals')
    op.drop_table('quiz_sessions')
    op.drop_table('leaderboard')
    op.drop_table('users')
    op.drop_table('quiz_questions')
    op.drop_table('courses')
    # ### end Alembic commands ###