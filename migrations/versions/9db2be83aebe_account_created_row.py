"""account created row

Revision ID: 9db2be83aebe
Revises: 8e3f4d4fc351
Create Date: 2022-10-25 08:43:23.637467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9db2be83aebe'
down_revision = '8e3f4d4fc351'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('account_created', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_account_created'), 'user', ['account_created'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_account_created'), table_name='user')
    op.drop_column('user', 'account_created')
    # ### end Alembic commands ###
