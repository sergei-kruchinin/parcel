"""Change Float to DECIMAL for certain fields

Revision ID: 82700929301f
Revises: 9f7c6009b542
Create Date: 2024-11-08 22:57:53.260174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '82700929301f'
down_revision: Union[str, None] = '9f7c6009b542'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parcels', 'weight',
               existing_type=mysql.FLOAT(),
               type_=sa.DECIMAL(precision=8, scale=3),
               existing_nullable=False)
    op.alter_column('parcels', 'value',
               existing_type=mysql.FLOAT(),
               type_=sa.DECIMAL(precision=9, scale=2),
               existing_nullable=False)
    op.alter_column('parcels', 'shipping_cost',
               existing_type=mysql.FLOAT(),
               type_=sa.DECIMAL(precision=9, scale=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parcels', 'shipping_cost',
               existing_type=sa.DECIMAL(precision=9, scale=2),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    op.alter_column('parcels', 'value',
               existing_type=sa.DECIMAL(precision=9, scale=2),
               type_=mysql.FLOAT(),
               existing_nullable=False)
    op.alter_column('parcels', 'weight',
               existing_type=sa.DECIMAL(precision=8, scale=3),
               type_=mysql.FLOAT(),
               existing_nullable=False)
    # ### end Alembic commands ###
