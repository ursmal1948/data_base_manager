"""add table trips

Revision ID: 11e4c7d4c81a
Revises: 
Create Date: 2024-05-31 23:16:44.902295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '11e4c7d4c81a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'trips',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('destination', sa.String(50), nullable=False),
        sa.Column('price', sa.DECIMAL),
        sa.Column('tourists_number', sa.Integer, default=0),
        sa.Column('agency_id', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('trips')
