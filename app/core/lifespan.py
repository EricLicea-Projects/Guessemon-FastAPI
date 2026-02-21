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
        encoding="utf8",
        decode_responses=True,
    )
    try:
        await r.ping()
    except RedisError as e:
        await r.aclose()
        raise RuntimeError(f"Redis is unavailable at {settings.REDIS_URL}") from e

    app.state.redis = r

async def close_redis(app: FastAPI) -> None:
    r = getattr(app.state, "redis", None)
    if r is not None:
        await r.aclose()
        app.state.redis = None

async def init_postgres(app: FastAPI) -> None:
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    await init_pg_pool(app, dsn=str(settings.DATABASE_URL))

    try:
        async with app.state.pg_pool.acquire() as conn:
            await conn.fetchval("SELECT 1;")
    except Exception as e:
        await close_pg_pool(app)
        raise RuntimeError(f"Postgres is unavailable at {settings.DATABASE_URL}") from e

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
