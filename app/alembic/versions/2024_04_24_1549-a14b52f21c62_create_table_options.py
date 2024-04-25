"""create_table_options

Revision ID: a14b52f21c62
Revises: 0ef8df982419
Create Date: 2024-04-24 15:49:35.083719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a14b52f21c62'
down_revision: Union[str, None] = '0ef8df982419'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'options_table',
        sa.Column('option_id', sa.Integer(),  nullable=False, unique=True, autoincrement=True, primary_key=True),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('option_value', sa.Text(), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=False),
        sa.Column('is_correct', sa.SmallInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('deleted', sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column('record_status', sa.SmallInteger(), nullable=False, server_default=sa.text("1")),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('updated_by_id', sa.Integer()),
        sa.PrimaryKeyConstraint('option_id'),
        sa.ForeignKeyConstraint(['question_id'], ['questions_table.question_id'])
    )


def downgrade():
    op.drop_table('options_table')