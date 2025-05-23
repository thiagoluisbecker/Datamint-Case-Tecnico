"""Tabela Genero

Revision ID: 0cf8a37c657b
Revises: 99db44cc9983
Create Date: 2025-05-13 22:19:06.283373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cf8a37c657b'
down_revision = '99db44cc9983'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('filmes', schema=None) as batch_op:
        batch_op.drop_column('genero')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('filmes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genero', sa.VARCHAR(length=50), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
