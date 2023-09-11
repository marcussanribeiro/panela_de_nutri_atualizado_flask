"""empty message

Revision ID: ba4fb616e298
Revises: 6bb793e7211e
Create Date: 2023-09-10 22:51:41.493763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba4fb616e298'
down_revision = '6bb793e7211e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Parceiros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('logomarca', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Portfolios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imagem', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('servicos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('resumo', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('servicos')
    op.drop_table('Portfolios')
    op.drop_table('Parceiros')
    # ### end Alembic commands ###