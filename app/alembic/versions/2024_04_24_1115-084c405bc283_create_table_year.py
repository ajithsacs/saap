"""create_table_year

Revision ID: 084c405bc283
Revises: 73cc05de5f13
Create Date: 2024-04-24 11:15:51.341057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '084c405bc283'
down_revision: Union[str, None] = '73cc05de5f13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'subject_years',
        sa.Column('year_id', sa.Integer(),  nullable=False, unique=True, autoincrement=True, primary_key=True),
        sa.Column('year_number', sa.Integer(), nullable=False),
        sa.Column('assessment_specification',  sa.String(255),nullable =False),
        sa.Column('subject_id', sa.Integer(), sa.ForeignKey('subject.subject_id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('deleted', sa.SmallInteger(), nullable=False, server_default=sa.text('0')),
        sa.Column('record_status', sa.SmallInteger(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('updated_by_id', sa.Integer()),
        sa.PrimaryKeyConstraint('year_id')
                )


def downgrade() -> None:
     op.drop_table('subject_years')
