"""empty message

Revision ID: 2ddb7d916cf5
Revises: 53a15054061e
Create Date: 2019-12-21 16:19:10.290935

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2ddb7d916cf5"
down_revision = "53a15054061e"
branch_labels = None
depends_on = None


def create_enum_type_if_not_exists(enum_type):
    context = op.get_context()
    if context.bind.dialect.name == "postgresql":
        has_size_type = context.bind.execute(
            f"select exists (select 1 from pg_type  where typname='{enum_type}')"
        ).scalar()
        if not has_size_type:
            op.execute(f"CREATE TYPE {enum_type} AS ENUM ('retail', 'wholesale')")
    else:
        print(f"context {context.bind.dialect.name} different than postgresql!")


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    create_enum_type_if_not_exists("usertype")
    op.add_column(
        "users",
        sa.Column(
            "user_type", sa.Enum("retail", "wholesale", name="usertype"), nullable=True
        ),
    )
    op.execute(f"UPDATE users SET user_type='retail'")
    op.alter_column("users", "user_type", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    create_enum_type_if_not_exists("usertype")
    op.drop_column("users", "user_type")
    # ### end Alembic commands ###
