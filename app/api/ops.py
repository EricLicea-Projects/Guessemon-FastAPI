import asyncpg
import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Security, Depends, Path

from app.api.deps import get_redis, get_pg_conn, get_http_client
from app.services.grand_archive_service import get_omni_local_event
from app.core.security import require_api_key
from app.cache.redis_cache import clear_redis_cache
from app.mappers import omni_event_mapper as oem


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


@router.get('/get_omni_event/{event_id}')
async def get_omni_event(
    event_id: int = Path(..., ge=1),
    client: httpx.AsyncClient = Depends(get_http_client),
    _: None = Security(require_api_key),
):
    data = await get_omni_local_event(client, event_id)
    # mapped_event = oem.map_event(data.event)
    # mapped_players = oem.map_players(data.players)
    # mapped_standings = oem.map_standings(event_id, data.standings)
    mapped_participants = oem.map_participants(event_id, data.rounds)

    return mapped_participants