"""add multilingual name and description

Revision ID: cc17af5482e8
Revises: f724444db69e
Create Date: 2026-09-22 02:04:10.181943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc17af5482e8'
down_revision: Union[str, None] = 'f724444db69e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Les anciennes valeurs texte ne sont pas du JSON valide : on vide les tables de test
    op.execute("DELETE FROM products;")
    op.execute("DELETE FROM categories;")
    op.alter_column('categories', 'name', existing_type=sa.String(length=100), type_=sa.Text(), nullable=False)
    op.alter_column('products', 'name', existing_type=sa.String(length=150), type_=sa.Text(), nullable=False)
    # description était déjà TEXT — aucun changement de type physique nécessaire


def downgrade() -> None:
    op.alter_column('products', 'name', existing_type=sa.Text(), type_=sa.String(length=150), nullable=False)
    op.alter_column('categories', 'name', existing_type=sa.Text(), type_=sa.String(length=100), nullable=False)