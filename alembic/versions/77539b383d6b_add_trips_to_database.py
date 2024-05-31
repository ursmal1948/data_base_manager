"""add trips to database

Revision ID: 77539b383d6b
Revises: 11e4c7d4c81a
Create Date: 2024-05-31 23:37:12.774577

"""
from typing import Sequence, Union
from decimal import Decimal
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '77539b383d6b'
down_revision: Union[str, None] = '11e4c7d4c81a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("insert into trips (destination, price, tourists_number, agency_id) values ('USA',1000,30,1)")
    op.execute("insert into trips (destination, price, tourists_number, agency_id) values ('EGIPT',500,150,2)")


def downgrade() -> None:
    op.execute(
        "delete from trips where destination = 'USA' and price = 1000 and tourists_number = 30 and agency_id = 1")
    op.execute(
        "delete from trips where destination = 'EGIPT' and price = 500 and tourists_number = 150 and agency_id = 2")