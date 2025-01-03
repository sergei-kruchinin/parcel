"""Change parcel ID from UUID to ULID

Revision ID: 9f7c6009b542
Revises: f92ffae60c22
Create Date: 2024-11-08 20:47:01.501587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9f7c6009b542'
down_revision: Union[str, None] = 'f92ffae60c22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Временное удаление ограничения PRIMARY KEY для изменения типа
    op.drop_constraint('parcels_pkey', 'parcels', type_='primary')

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parcel_types', 'id',
               existing_type=mysql.INTEGER(),
               comment='Уникальный идентификатор типа посылки',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('parcel_types', 'name',
               existing_type=mysql.VARCHAR(length=50),
               comment='Имя типа посылки, уникальное',
               existing_nullable=False)
    op.alter_column('parcels', 'id',
               existing_type=sa.BINARY(length=16),
               type_=sa.String(length=26),
               existing_nullable=False)
    # ### end Alembic commands ###

    # Восстановление PRIMARY KEY ограничения
    op.create_primary_key('parcels_pkey', 'parcels', ['id'])

def downgrade() -> None:
    # Временное удаление ограничения PRIMARY KEY для восстановления старого типа
    op.drop_constraint('parcels_pkey', 'parcels', type_='primary')

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parcels', 'id',
               existing_type=sa.String(length=26),
               type_=sa.BINARY(length=16),
               existing_nullable=False)
    op.alter_column('parcel_types', 'name',
               existing_type=mysql.VARCHAR(length=50),
               comment=None,
               existing_comment='Имя типа посылки, уникальное',
               existing_nullable=False)
    op.alter_column('parcel_types', 'id',
               existing_type=mysql.INTEGER(),
               comment=None,
               existing_comment='Уникальный идентификатор типа посылки',
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###

    # Восстановление PRIMARY KEY ограничения
    op.create_primary_key('parcels_pkey', 'parcels', ['id'])
