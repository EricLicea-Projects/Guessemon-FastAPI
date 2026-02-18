import asyncpg
import redis.asyncio as redis
from fastapi import APIRouter, Security, Depends

from app.api.deps import get_redis, get_pg_conn
from app.core.security import require_api_key
from app.cache.redis_cache import clear_redis_cache


router = APIRouter(tags = ['ops'])

@router.post('/clear_cache')
async def clear_cache(
    r:redis.Redis = Depends(get_redis),
    _: None = Security(require_api_key)
):
    
    await clear_redis_cache(r)
    return {'Message': 'Redis cache cleared successfully.'}


@router.get('/db_ping')
async def db_ping(
    conn: asyncpg.Connection = Depends(get_pg_conn),
    _: None = Security(require_api_key),
):
    
    value = await conn.fetchval('SELECT 1;')
    return {'OK': value == 1}