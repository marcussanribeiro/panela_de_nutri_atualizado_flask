"""empty message

Revision ID: 9cceb6188cf8
Revises: 
Create Date: 2023-08-03 11:58:08.761280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cceb6188cf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conteudos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('capa', sa.String(length=100), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('resumo', sa.String(length=1000), nullable=False),
    sa.Column('logradouro', sa.String(length=1000), nullable=False),
    sa.Column('token', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('usuarios',
    sa.Column('foto', sa.String(length=100), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('sobrenome', sa.String(length=100), nullable=False),
    sa.Column('funcao', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('senha', sa.String(length=100), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subconteudos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sub_imagem', sa.String(length=100), nullable=False),
    sa.Column('sub_titulo', sa.String(length=100), nullable=False),
    sa.Column('sub_conteudo', sa.String(length=10000), nullable=False),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['token_id'], ['conteudos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subconteudos')
    op.drop_table('usuarios')
    op.drop_table('conteudos')
    # ### end Alembic commands ###