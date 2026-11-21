"""Create the users table or adopt the schema from sql/001_users.sql."""

import sqlalchemy as sa
from alembic import op

revision = "0001_create_users"
down_revision = None
branch_labels = None
depends_on = None

TABLE_NAME = "users"
CATEGORY_CHECK = "users_category_check"


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if inspector.has_table(TABLE_NAME):
        # The old Compose init script created this same schema and constraint name.
        columns = {column["name"]: column for column in inspector.get_columns(TABLE_NAME)}
        expected = {
            "telegram_id": (sa.BigInteger, False),
            "first_name": (sa.Text, True),
            "last_name": (sa.Text, True),
            "username": (sa.Text, True),
            "category": (sa.Text, True),
            "created_at": (sa.DateTime, False),
        }
        valid_columns = columns.keys() == expected.keys() and all(
            isinstance(columns[name]["type"], kind) and columns[name]["nullable"] == nullable
            for name, (kind, nullable) in expected.items()
        )
        primary_key = inspector.get_pk_constraint(TABLE_NAME)["constrained_columns"]
        checks = inspector.get_check_constraints(TABLE_NAME)
        created_at = columns.get("created_at")
        created_at_type = created_at["type"] if created_at else None
        if (
            not valid_columns
            or primary_key != ["telegram_id"]
            or not isinstance(created_at_type, sa.DateTime)
            or not created_at_type.timezone
            or columns["created_at"]["default"] != "now()"
            or not any(check["name"] == CATEGORY_CHECK for check in checks)
        ):
            raise RuntimeError("Existing users table does not match the legacy bot schema.")
        return

    op.create_table(
        TABLE_NAME,
        sa.Column("telegram_id", sa.BigInteger(), primary_key=True, autoincrement=False),
        sa.Column("first_name", sa.Text()),
        sa.Column("last_name", sa.Text()),
        sa.Column("username", sa.Text()),
        sa.Column("category", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("category IN ('OGE', 'EGE')", name=CATEGORY_CHECK),
    )


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
