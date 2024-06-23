from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from odmantic.session import AIOSession

from conf import settings


@lru_cache(maxsize=1)
def get_db_adapter():
    return DBAdapter()


class DBAdapter:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.DATABASE_URL)
        self.engine = AIOEngine(client=self.client, database=settings.DB_NAME)

    async def connect(self):
        await self.ping()

    def disconnect(self):
        self.client.close()

    async def ping(self):
        try:
            async with self.engine.session():
                return
        except Exception as exc:
            raise ConnectionError("Could not connect to the database") from exc

    @asynccontextmanager
    async def session(self):
        async with self.engine.session() as session:
            yield session

    @property
    def Session(self):
        return Annotated[AIOSession, Depends(self.session)]
