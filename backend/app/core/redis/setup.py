from typing import Optional

import redis.asyncio as redis

import config

pool: Optional[redis.ConnectionPool] = None
connections: list[redis.Redis] = []


def setup():
    global pool
    pool = redis.ConnectionPool.from_url(
        config.env_param('REDIS_URL')
    )


def ensure_pool_setup(func):
    def wrapper():
        if pool is None:
            setup()

        return func()

    return wrapper


async def stop():
    for connection in connections:
        await connection.aclose()
    await pool.aclose()


@ensure_pool_setup
def get_connection():
    global connections
    connection = redis.Redis(
        connection_pool=pool,
        protocol=3
    )
    connections.append(connection)
    return connection

