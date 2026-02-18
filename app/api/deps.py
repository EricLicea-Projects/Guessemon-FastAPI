from typing import AsyncGenerator
from fastapi import Request
import redis.asyncio as redis
import asyncpg

def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis

async def get_pg_conn(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    pool = getattr(request.app.state, "pg_pool", None)
    if pool is None:
        raise RuntimeError("Postgres pool is not initialized. Did lifespan call init_pg_pool()?")
    async with pool.acquire() as conn:
        yield conn
