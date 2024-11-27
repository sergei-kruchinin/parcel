"""add initial package types data

Revision ID: f92ffae60c22
Revises: 4cc0f35b3a19
Create Date: 2024-11-07 19:24:55.321625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f92ffae60c22'
down_revision: Union[str, None] = '4cc0f35b3a19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    package_types_table = sa.table('parcel_types',
                                   sa.column('name', sa.String)
                                   )

    # Вставляем начальные данные
    op.bulk_insert(
        package_types_table,
        [
            {'name': 'одежда'},
            {'name': 'электроника'},
            {'name': 'разное'},
        ]
    )


def downgrade() -> None:
    op.execute('DELETE FROM parcel_types WHERE name IN ("одежда", "электроника", "разное")')
