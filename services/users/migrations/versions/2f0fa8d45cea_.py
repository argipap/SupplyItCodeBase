"""empty message

Revision ID: 2f0fa8d45cea
Revises: 2ddb7d916cf5
Create Date: 2019-12-23 20:32:24.448703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f0fa8d45cea"
down_revision = "2ddb7d916cf5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("suppliers_to_retailers")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "suppliers_to_retailers",
        sa.Column("supplier_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("retailer_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
