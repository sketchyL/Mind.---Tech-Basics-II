"""2nd try add alt text column

Revision ID: 4ce7f40d858f
Revises: 54e5cf41fb7b
Create Date: 2023-02-11 12:56:38.936875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ce7f40d858f'
down_revision = '54e5cf41fb7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cat_img_alt_text', sa.Text(), nullable=True))
        batch_op.drop_column('cat_description')

    with op.batch_alter_table('lib_med', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cover_alt_text', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lib_med', schema=None) as batch_op:
        batch_op.drop_column('cover_alt_text')

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cat_description', sa.TEXT(), nullable=True))
        batch_op.drop_column('cat_img_alt_text')

    # ### end Alembic commands ###
