"""remove user table public_id

Revision ID: e46f433510f9
Revises: 1c4a9139a00d
Create Date: 2019-10-26 13:26:28.865167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e46f433510f9'
down_revision = '1c4a9139a00d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('public_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('public_id', sa.VARCHAR(length=100), nullable=True))
    # ### end Alembic commands ###
