"""add alt text column

Revision ID: 54e5cf41fb7b
Revises: 18d582182035
Create Date: 2023-02-11 12:52:09.022570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e5cf41fb7b'
down_revision = '18d582182035'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('cat_img_url',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('cat_img_url',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###