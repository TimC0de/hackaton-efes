from typing import Optional
import motor.motor_asyncio
import os

import config
from .collection import Collection

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.__client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]
        
    @property
    def raw_client(self):
        return self.__client
        
    def collection(self, collection: str) -> Collection:
        return Collection(self.__db[collection])

    async def close(self):
        self.__client.close()

client: Optional[MongoDB] = None

def get_client() -> Optional[MongoDB]:
    return client


def connect():
    global client

    client = MongoDB(config.env_param('MONGODB_URL'), config.env_param('MONGODB_DATABASE'))


async def close():
    await client.close()
