"""add foreign key parameter

Revision ID: 6517c4e2837d
Revises: a71d3fdd56ad
Create Date: 2023-01-29 15:56:03.619152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6517c4e2837d'
down_revision = 'a71d3fdd56ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('med_favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('med_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['med_id'], ['lib_med.id'], name=op.f('fk_med_favorite_med_id_lib_med')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_med_favorite_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_med_favorite'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('med_favorite')
    # ### end Alembic commands ###
