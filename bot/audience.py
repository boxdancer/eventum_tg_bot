from datetime import datetime

from constants.audience import AudienceCategory
from logger_config import get_logger
from sqlalchemy import Text, func, literal, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql import ColumnElement
from telegram import User

from bot.db.models import UserCategoryModel, UserModel
from bot.db.session import database_url

logger = get_logger(__name__)


class Audience:
    def __init__(self):
        self.engine = create_async_engine(
            database_url(),
            pool_pre_ping=True,
            pool_size=4,
            max_overflow=0,
            connect_args={"command_timeout": 10},
        )
        self.sessions = async_sessionmaker(self.engine)

    async def open(self):
        async with self.engine.connect():
            pass

    async def close(self):
        await self.engine.dispose()

    async def save_user(self, user: User):
        stmt = insert(UserModel).values(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[UserModel.telegram_id],
            set_={
                UserModel.first_name: stmt.excluded.first_name,
                UserModel.last_name: stmt.excluded.last_name,
                UserModel.username: stmt.excluded.username,
            },
        )
        await self._write(stmt, user.id)

    async def add_category(self, telegram_id: int, category: AudienceCategory):
        user_selection = select(UserModel.telegram_id, literal(category, type_=Text())).where(
            UserModel.telegram_id == telegram_id
        )
        stmt = (
            insert(UserCategoryModel)
            .from_select(
                [UserCategoryModel.telegram_id, UserCategoryModel.category], user_selection
            )
            .on_conflict_do_nothing(
                index_elements=[UserCategoryModel.telegram_id, UserCategoryModel.category]
            )
        )
        await self._write(stmt, telegram_id)

    async def _write(self, stmt, telegram_id: int):
        try:
            async with self.sessions.begin() as session:
                await session.execute(stmt)
        except SQLAlchemyError, OSError, TimeoutError:
            logger.exception("Could not save audience data for Telegram ID %s", telegram_id)

    @staticmethod
    def _segment(category: AudienceCategory | None, since: datetime | None):
        conditions: list[ColumnElement[bool]] = []
        if category is not None:
            membership = select(UserCategoryModel.telegram_id).where(
                UserCategoryModel.telegram_id == UserModel.telegram_id,
                UserCategoryModel.category == category,
            )
            conditions.append(membership.exists())
        if since is not None:
            conditions.append(UserModel.created_at >= since)
        return conditions

    async def count(self, category: AudienceCategory | None, since: datetime | None) -> int:
        stmt = select(func.count()).select_from(UserModel).where(*self._segment(category, since))
        async with self.sessions() as session:
            result = await session.execute(stmt)
            return result.scalar_one()

    async def page(
        self,
        category: AudienceCategory | None,
        since: datetime | None,
        *,
        offset: int,
        limit: int,
    ) -> list[UserModel]:
        stmt = (
            select(UserModel)
            .where(*self._segment(category, since))
            .order_by(UserModel.created_at.desc(), UserModel.telegram_id.desc())
            .offset(offset)
            .limit(limit)
        )
        async with self.sessions() as session:
            return list(await session.scalars(stmt))

    async def recipient_ids(
        self, category: AudienceCategory | None, since: datetime | None
    ) -> list[int]:
        stmt = (
            select(UserModel.telegram_id)
            .where(*self._segment(category, since))
            .order_by(UserModel.telegram_id)
        )
        async with self.sessions() as session:
            return list(await session.scalars(stmt))
