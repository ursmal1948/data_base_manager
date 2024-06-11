"""add tests trips

Revision ID: cfc6e8e43f39
Revises: 93af0856a474
Create Date: 2024-06-11 13:15:25.612240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfc6e8e43f39'
down_revision: Union[str, None] = '93af0856a474'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("insert into trips (destination, price, tourists_number,agency_id) values ('USA',1000,30,1)")
    op.execute("insert into trips (destination, price, tourists_number,agency_id) values ('EGIPT',500,150,2)")



def downgrade() -> None:
    op.execute(
        "delete from trips where destination='USA' and price=1000 and tourists_number=30 and agency_id=1"
    )
    op.execute(
        "delete from trips where destination='EGIPT' and price=500 and tourists_number=150 and agency_id=2"
    )
