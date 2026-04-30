from collections.abc import AsyncGenerator
from typing import cast

import asyncpg
import httpx
import redis.asyncio as redis
from fastapi import Request


def get_http_client(request: Request) -> httpx.AsyncClient:
    client = getattr(request.app.state, "http_client", None)

    if client is None:
        raise RuntimeError(
            "HTTP client is not initialized. Did lifespan call init_http_client()?"
        )

    return cast(httpx.AsyncClient, client)


def get_redis(request: Request) -> redis.Redis:
    r = getattr(request.app.state, "redis", None)

    if r is None:
        raise RuntimeError(
            "Redis client is not initialized. Did lifespan call init_redis()?"
        )

    return cast(redis.Redis, r)


async def get_pg_conn(
    request: Request,
) -> AsyncGenerator[asyncpg.Connection, None]:
    pool = getattr(request.app.state, "pg_pool", None)

    if pool is None:
        raise RuntimeError(
            "Postgres pool is not initialized. Did lifespan call init_pg_pool()?"
        )

    async with pool.acquire() as conn:
        yield conn