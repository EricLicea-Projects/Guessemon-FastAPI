from contextlib import asynccontextmanager

import httpx
import redis.asyncio as redis
from redis.exceptions import RedisError
from fastapi import FastAPI

from app.core.settings import settings
from app.db.postgres import init_pg_pool, close_pg_pool

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)
DEFAULT_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)

async def init_redis(app: FastAPI) -> None:
    r = redis.from_url(
        str(settings.REDIS_URL),
        encoding="utf-8",
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        health_check_interval=30,
    )

    try:
        await r.ping()
    except RedisError as e:
        await r.aclose()
        raise RuntimeError("Redis is unavailable") from e

    app.state.redis = r

async def close_redis(app: FastAPI) -> None:
    r = getattr(app.state, "redis", None)
    if r is not None:
        await r.aclose()
        app.state.redis = None

async def init_postgres(app: FastAPI) -> None:
    await init_pg_pool(app, dsn=str(settings.DATABASE_URL))

    try:
        async with app.state.pg_pool.acquire() as conn:
            await conn.fetchval("SELECT 1;")
    except Exception as e:
        await close_pg_pool(app)
        raise RuntimeError("Postgres is unavailable") from e

async def close_postgres(app: FastAPI) -> None:
    pool = getattr(app.state, "pg_pool", None)
    if pool is not None:
        await close_pg_pool(app)
        app.state.pg_pool = None

async def init_http_client(app: FastAPI) -> None:
    app.state.http_client = httpx.AsyncClient(
        timeout=DEFAULT_TIMEOUT,
        limits=DEFAULT_LIMITS,
        http2=True,
    )

async def close_http_client(app: FastAPI) -> None:
    client = getattr(app.state, "http_client", None)
    if client is not None:
        await client.aclose()
        app.state.http_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = None
    app.state.pg_pool = None
    app.state.http_client = None

    try:
        await init_redis(app)
        await init_postgres(app)
        await init_http_client(app)
        yield
    finally:
        await close_http_client(app)
        await close_postgres(app)
        await close_redis(app)
