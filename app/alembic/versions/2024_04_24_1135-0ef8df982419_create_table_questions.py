"""create_table_questions

Revision ID: 0ef8df982419
Revises: 084c405bc283
Create Date: 2024-04-24 11:35:40.919242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ef8df982419'
down_revision: Union[str, None] = '084c405bc283'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'questions_table',
        sa.Column('question_id', sa.Integer(), nullable=False, unique=True, autoincrement=True, primary_key=True),
        sa.Column('subject_id', sa.Integer(), sa.ForeignKey('subject.subject_id'), nullable=False),
        sa.Column('year_id', sa.Integer(), sa.ForeignKey('subject_years.year_id'), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('deleted', sa.SmallInteger(), nullable=False, server_default=sa.text('0')),
        sa.Column('record_status', sa.SmallInteger(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('updated_by_id', sa.Integer()),
        sa.PrimaryKeyConstraint('question_id')
    )

def downgrade():
    op.drop_table('questions_table')
