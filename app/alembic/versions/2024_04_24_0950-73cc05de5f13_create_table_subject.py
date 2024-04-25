"""create_table_subject

Revision ID: 73cc05de5f13
Revises: 
Create Date: 2024-04-24 09:50:45.555426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73cc05de5f13'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'subject',
        sa.Column('subject_id',sa.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True),
        sa.Column('subject_name', sa.String(255), index=True, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('deleted', sa.SmallInteger, nullable=False, server_default=sa.text("0")),
        sa.Column('record_status', sa.SmallInteger, nullable=False, server_default=sa.text("1")),
        sa.Column('created_by_id', sa.Integer, nullable=False),
        sa.Column('updated_by_id', sa.Integer),
        sa.PrimaryKeyConstraint('subject_id')

    )

def downgrade():
    op.drop_table('subject')



