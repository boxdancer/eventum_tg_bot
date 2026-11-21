from datetime import datetime

from constants.audience import AudienceCategory
from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, Text, column, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    first_name: Mapped[str | None] = mapped_column(Text)
    last_name: Mapped[str | None] = mapped_column(Text)
    username: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserCategoryModel(Base):
    __tablename__ = "user_categories"

    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(UserModel.telegram_id, ondelete="CASCADE"),
        primary_key=True,
    )
    category: Mapped[str] = mapped_column(Text, primary_key=True)

    __table_args__ = (
        Index("ix_user_categories_category_telegram_id", "category", "telegram_id"),
        CheckConstraint(
            column("category", Text).in_(tuple(AudienceCategory)),
            name="user_categories_category_check",
        ),
    )
