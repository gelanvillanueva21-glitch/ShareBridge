"""add_profile_search_indexes

Revision ID: babce3613636
Revises: fad8b2c30fd7
Create Date: 2026-09-27 05:08:25.469767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'babce3613636'
down_revision: Union[str, None] = 'fad8b2c30fd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
