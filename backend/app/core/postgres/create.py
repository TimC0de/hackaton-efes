import logging

from app.core.postgres.models.base import Base

from app.core.postgres.setup import engine

import config

from app.api.security.hash import get_password_hash
from app.core.postgres.models import user
from app.core.postgres.models.user import Role, User
from app.core.postgres.queries import role as role_queries, user as user_queries

logger = logging.getLogger('app.core.postgres.create')

async def create_tables():
    from app.core.postgres.models.user import User, Role  # Import models to ensure they are registered
    async with engine.begin() as conn:
        # Run the create_all inside the async engine context
        await conn.run_sync(Base.metadata.create_all)


async def create_roles():
    for role in user.Roles:
        await role_queries.insert_if_not_exists(Role(name=role.name))


async def create_admin():
    username = config.env_param('ADMIN_USERNAME')
    password = config.env_param('ADMIN_PASSWORD')

    roles = await role_queries.get_by_names(user.Roles.ADMIN.value)
    await user_queries.insert_if_not_exists(
        User(
            username=username,
            hashed_password=get_password_hash(password),
            roles=roles
        )
    )
