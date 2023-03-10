"""new

Revision ID: aaa631e4930c
Revises: bf51b4a994df
Create Date: 2023-01-15 12:49:26.785402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaa631e4930c'
down_revision = 'bf51b4a994df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lib_med', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.Integer(), nullable=True))
        batch_op.alter_column('category',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.create_foreign_key(None, 'categories', ['category'], ['id'])
        batch_op.drop_column('length')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lib_med', schema=None) as batch_op:
        batch_op.add_column(sa.Column('length', sa.FLOAT(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('category',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.drop_column('time')

    # ### end Alembic commands ###
