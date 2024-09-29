from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import config

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{config.env_param("DB_USERNAME")}:{config.env_param("DB_PASSWORD")}@{config.env_param("DB_HOST")}:{config.env_param("DB_PORT")}/{config.env_param("DB_NAME")}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    pool_recycle=3600
)

# Each instance of the SessionLocal class will be a database session
AsyncSessionFactory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
