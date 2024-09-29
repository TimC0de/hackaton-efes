from typing import Optional

from sqlalchemy import select

from app.core.postgres.setup import AsyncSessionFactory

from app.core.postgres.models.user import Role


async def get_by_names(*names: str) -> list[Role]:
    async with AsyncSessionFactory() as session:
        async with session.begin():
            result = await session.execute(select(Role).filter(Role.name.in_(names)))
            return result.scalars().all()


async def insert_if_not_exists(role: Role):
    async with AsyncSessionFactory() as session:
        async with session.begin():
            result = await session.execute(select(Role).filter(Role.name == role.name))
            existing_role = result.scalars().first()

            if not existing_role:
                session.add(role)
                await session.commit()
