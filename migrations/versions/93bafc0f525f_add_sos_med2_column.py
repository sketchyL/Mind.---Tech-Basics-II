"""add sos_med2 column

Revision ID: 93bafc0f525f
Revises: 1b537bf709ce
Create Date: 2023-01-28 11:07:25.005487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93bafc0f525f'
down_revision = '1b537bf709ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sos_med2', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_user_sos_med2_lib_med'), 'lib_med', ['sos_med2'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_user_sos_med2_lib_med'), type_='foreignkey')
        batch_op.drop_column('sos_med2')

    # ### end Alembic commands ###
