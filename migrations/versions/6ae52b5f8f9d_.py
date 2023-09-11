"""empty message

Revision ID: 6ae52b5f8f9d
Revises: 9cceb6188cf8
Create Date: 2023-08-03 12:06:13.276875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ae52b5f8f9d'
down_revision = '9cceb6188cf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('foto',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('foto',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###