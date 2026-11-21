"""Record all distinct exam categories selected by a user."""

import sqlalchemy as sa
from alembic import op

revision = "0002_user_categories"
down_revision = "0001_create_users"
branch_labels = None
depends_on = None

USERS = "users"
USER_CATEGORIES = "user_categories"
CATEGORY_INDEX = "ix_user_categories_category_telegram_id"
CATEGORY_VALUES = "category IN ('OGE', 'EGE')"


def upgrade() -> None:
    memberships = op.create_table(
        USER_CATEGORIES,
        sa.Column("telegram_id", sa.BigInteger(), primary_key=True, autoincrement=False),
        sa.Column("category", sa.Text(), primary_key=True),
        sa.ForeignKeyConstraint(["telegram_id"], [f"{USERS}.telegram_id"], ondelete="CASCADE"),
        sa.CheckConstraint(CATEGORY_VALUES, name="user_categories_category_check"),
    )
    users = sa.table(
        USERS, sa.column("telegram_id", sa.BigInteger()), sa.column("category", sa.Text())
    )
    op.execute(
        sa.insert(memberships).from_select(
            ["telegram_id", "category"],
            sa.select(users.c.telegram_id, users.c.category).where(users.c.category.is_not(None)),
        )
    )
    op.create_index(CATEGORY_INDEX, USER_CATEGORIES, ["category", "telegram_id"])
    op.drop_column(USERS, "category")


def downgrade() -> None:
    users = sa.table(
        USERS, sa.column("telegram_id", sa.BigInteger()), sa.column("category", sa.Text())
    )
    memberships = sa.table(
        USER_CATEGORIES, sa.column("telegram_id", sa.BigInteger()), sa.column("category", sa.Text())
    )
    duplicates = (
        sa.select(memberships.c.telegram_id)
        .group_by(memberships.c.telegram_id)
        .having(sa.func.count() > 1)
        .exists()
    )
    if op.get_bind().scalar(sa.select(duplicates)):
        raise RuntimeError(
            "Cannot restore a single category while users belong to both categories."
        )

    op.add_column(USERS, sa.Column("category", sa.Text()))
    op.create_check_constraint("users_category_check", USERS, CATEGORY_VALUES)
    op.execute(
        sa.update(users)
        .where(users.c.telegram_id == memberships.c.telegram_id)
        .values(category=memberships.c.category)
    )
    op.drop_table(USER_CATEGORIES)
