"""create_table_question_type

Revision ID: 36badc83907f
Revises: a14b52f21c62
Create Date: 2024-04-24 16:45:28.508810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36badc83907f'
down_revision: Union[str, None] = 'a14b52f21c62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'question_type',
        sa.Column('question_type_id', sa.Integer(),  nullable=False, unique=True, autoincrement=True, primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('deleted', sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column('record_status', sa.SmallInteger(), nullable=False, server_default=sa.text("1")),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('updated_by_id', sa.Integer()),
        sa.PrimaryKeyConstraint('question_type_id'),
    )


def downgrade():
    op.drop_table('question_type')
