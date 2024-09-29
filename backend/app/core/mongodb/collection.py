from typing import Any, Optional

from pydantic import BaseModel

class Collection:
    
    def __init__(self, collection):
        self.__collection = collection
        
    @property
    def raw_collection(self):
        return self.__collection
        
    async def insert(self, values: dict[str, Any]):
        await self.__collection.insert_one(values)

    async def insert_many(self, values: list[dict[str, Any]]):
        await self.__collection.insert_many(values)
        
    async def count(self):
        count = await self.__collection.count_documents({})
        return count
        
    async def update(self, filter: dict[str, Any], values: dict[str, Any]):
        await self.__collection.update_one(filter, {"$set": values})
        
    async def append(self, filter: dict[str, Any], list_name: str, value: Any):
        await self.__collection.update_one(filter, {"$push": {list_name: value}})
        
    async def fetch_one(self, filter: dict[str, Any]) -> Optional[dict[str, Any]]:
        document = await self.__collection.find_one(filter)
        return document
    
    async def fetch_all(self, filter: dict[str, Any] = {}, sort: list[tuple[str, int]] = [], limit = 0) -> list[dict[str, Any]]:
        cursor = self.__collection.find(filter)

        if sort:
            cursor = cursor.sort(sort)

        documents = await cursor.limit(limit).to_list(None)
        return documents
    
    async def remove(self, filter: dict[str, Any]):
        await self.__collection.delete_one(filter)