from sqlalchemy import select, func, and_
from sqlalchemy.sql.functions import count

from app.core.postgres.setup import AsyncSessionFactory

from app.core.postgres.models.event import Event


async def insert(event: Event):
    async with AsyncSessionFactory() as session:
        async with session.begin():
            session.add(event)
            await session.commit()


async def get_all() -> list[Event]:
    async with AsyncSessionFactory() as session:
        async with session.begin():
            result = await session.execute(select(Event))
            return result.scalars().all()


async def get_strike_by_event(event: Event, user_id: int, filter_value: str) -> int:
    async with AsyncSessionFactory() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    count(Event.id).label('count')
                )
                .group_by(func.date(Event.timestamp))
                .filter(
                    and_(
                        func.date(Event.timestamp) == func.date(filter_value),
                        Event.name == event.value,
                        Event.user_id == user_id
                    )
                )
            )
            result = result.fetchone()
            return 0 if result is None else result[0]
