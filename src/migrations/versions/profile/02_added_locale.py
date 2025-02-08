"""02_added_locale_to_profile_model

Revision ID: a4f9f1984aaa
Revises: 28fe95bacc23
Create Date: 2025-02-06 15:36:04.071219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a4f9f1984aaa'
down_revision: Union[str, None] = '28fe95bacc23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    locale_enum = postgresql.ENUM('kyrgyz', 'russian', 'english', name='localeenum', create_type=False)
    locale_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('profile', sa.Column('locale', locale_enum, nullable=True))


def downgrade():
    locale_enum = postgresql.ENUM('kyrgyz', 'russian', 'english',name='localeenum', create_type=False)
    op.drop_column('profile', 'locale')
    locale_enum.drop(op.get_bind(), checkfirst=True)
