"""add sos_med3

Revision ID: ea78d808ed8d
Revises: 93bafc0f525f
Create Date: 2023-01-28 12:08:14.502845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea78d808ed8d'
down_revision = '93bafc0f525f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sos_med3', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_user_sos_med3_lib_med'), 'lib_med', ['sos_med3'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_user_sos_med3_lib_med'), type_='foreignkey')
        batch_op.drop_column('sos_med3')

    # ### end Alembic commands ###