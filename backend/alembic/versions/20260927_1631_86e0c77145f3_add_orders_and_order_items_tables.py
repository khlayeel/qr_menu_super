"""add orders and order_items tables

Revision ID: 86e0c77145f3
Revises: cc17af5482e8
Create Date: 2026-09-27 16:31:45.202678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86e0c77145f3'
down_revision: Union[str, None] = 'cc17af5482e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass