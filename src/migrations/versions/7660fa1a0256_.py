"""empty message

Revision ID: 7660fa1a0256
Revises: 
Create Date: 2024-06-21 21:09:49.184241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7660fa1a0256'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_values',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('values', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_values')
    # ### end Alembic commands ###
