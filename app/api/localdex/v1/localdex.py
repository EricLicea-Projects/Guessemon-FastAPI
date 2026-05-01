from typing import cast

from fastapi import APIRouter, Depends
import asyncpg
import redis.asyncio as redis

from app.api.deps import get_pg_pool, get_redis
from app.services.recent_standings import fetch_recent_standings
from app.db.local_dex.get_player_stats import get_player_stats
from app.db.local_dex.player_profile import player_profile
from app.cache.redis_cache import (
    get_data_version,
    get_or_set_json,
    make_cache_key,
)


router = APIRouter(tags=["LocalDex"])


@router.get("/standings")
async def get_recent_standings(
    r: redis.Redis = Depends(get_redis),
    pool: asyncpg.Pool = Depends(get_pg_pool),
):
    version = await get_data_version(r)
    cache_key = make_cache_key(version, "localdex:standings")

    async def fetch_from_db():
        async with pool.acquire() as conn:
            conn = cast(asyncpg.Connection, conn)
            return await fetch_recent_standings(conn)

    return await get_or_set_json(
        r,
        cache_key,
        fetch_from_db,
    )


@router.get("/player-stats")
async def get_player_stats_table(
    r: redis.Redis = Depends(get_redis),
    pool: asyncpg.Pool = Depends(get_pg_pool),
):
    version = await get_data_version(r)
    cache_key = make_cache_key(version, "localdex:player-stats")

    async def fetch_from_db():
        async with pool.acquire() as conn:
            conn = cast(asyncpg.Connection, conn)
            return await get_player_stats(conn)

    return await get_or_set_json(
        r,
        cache_key,
        fetch_from_db,
    )


@router.get("/player-profile/{player_id}")
async def get_player_profile(
    player_id: int,
    r: redis.Redis = Depends(get_redis),
    pool: asyncpg.Pool = Depends(get_pg_pool),
):
    version = await get_data_version(r)
    cache_key = make_cache_key(version, "localdex:player-profile", player_id)

    async def fetch_from_db():
        async with pool.acquire() as conn:
            conn = cast(asyncpg.Connection, conn)
            return await player_profile(conn, player_id)

    return await get_or_set_json(
        r,
        cache_key,
        fetch_from_db,
    )