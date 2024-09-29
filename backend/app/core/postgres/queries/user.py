from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.postgres.setup import AsyncSessionFactory

from app.core.postgres.models.user import User


async def insert_if_not_exists(user: User):
    async with AsyncSessionFactory() as session:
        async with session.begin():
            result = await session.execute(select(User).filter(User.username == user.username))
            existing_user = result.scalars().first()

            if not existing_user:
                session.add(user)
                await session.commit()
                await session.refresh(user)


async def get_by_username(username: str) -> Optional[User]:
    async with AsyncSessionFactory() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(joinedload(User.roles))
                .filter(User.username == username)
            )
            return result.scalars().first()