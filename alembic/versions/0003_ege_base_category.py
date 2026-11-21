"""Allow a separate audience category for the base EGE exam."""

import sqlalchemy as sa
from alembic import op

revision = "0003_ege_base_category"
down_revision = "0002_user_categories"
branch_labels = None
depends_on = None

TABLE_NAME = "user_categories"
CONSTRAINT_NAME = "user_categories_category_check"


def upgrade() -> None:
    op.drop_constraint(CONSTRAINT_NAME, TABLE_NAME, type_="check")
    op.create_check_constraint(
        CONSTRAINT_NAME, TABLE_NAME, "category IN ('OGE', 'EGE', 'EGE_BASE')"
    )


def downgrade() -> None:
    memberships = sa.table(TABLE_NAME, sa.column("category", sa.Text()))
    has_base_memberships = (
        sa.select(memberships.c.category).where(memberships.c.category == "EGE_BASE").exists()
    )
    if op.get_bind().scalar(sa.select(has_base_memberships)):
        raise RuntimeError("Cannot remove EGE_BASE while users belong to that category.")

    op.drop_constraint(CONSTRAINT_NAME, TABLE_NAME, type_="check")
    op.create_check_constraint(CONSTRAINT_NAME, TABLE_NAME, "category IN ('OGE', 'EGE')")
