"""add streakentry class, current streak, best streak

Revision ID: a05bc3ddcd23
Revises: 21a8d84c6bff
Create Date: 2023-01-17 16:01:37.243282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a05bc3ddcd23'
down_revision = '21a8d84c6bff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('streak_entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('streak_tick', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_streak_entry_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_streak_entry'))
    )
    with op.batch_alter_table('streak_entry', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_streak_entry_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index('ix_post_timestamp')

    op.drop_table('post')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('best_streak', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('current_streak', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('current_streak')
        batch_op.drop_column('best_streak')

    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index('ix_post_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('streak_entry', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_streak_entry_timestamp'))

    op.drop_table('streak_entry')
    # ### end Alembic commands ###