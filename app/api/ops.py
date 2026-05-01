import json
from datetime import UTC, datetime


import asyncpg
import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Security, Depends, Path, Body
from pydantic import BaseModel

from app.api.deps import get_redis, get_pg_conn, get_http_client
from app.services.grand_archive_service import get_omni_local_event
from app.core.security import require_api_key
from app.cache.redis_cache import clear_redis_cache
from app.cache.keys import MAINTENANCE_KEY
from app.cache.keys import DATA_VERSION_KEY
from app.mappers import omni_event_mapper as oem
from app.schemas.omni_event_data import OmniCrudPayload
from app.db.omni_event.event_transactions import event_transactions


router = APIRouter(tags=["Ops"])


class MaintenancePayload(BaseModel):
    message: str = "Currently updating data. Please check back soon."


@router.post("/maintenance/on")
async def maintenance_on(
    payload: MaintenancePayload,
    r: redis.Redis = Depends(get_redis),
    _: None = Security(require_api_key),
):
    await r.set(
        MAINTENANCE_KEY,
        json.dumps(
            {
                "enabled": True,
                "message": payload.message,
            }
        ),
    )

    return {
        "maintenance": True,
        "message": payload.message,
    }


@router.post("/maintenance/off")
async def maintenance_off(
    r: redis.Redis = Depends(get_redis),
    _: None = Security(require_api_key),
):
    await r.delete(MAINTENANCE_KEY)

    return {
        "maintenance": False,
        "message": "Maintenance mode disabled.",
    }


@router.post("/publish-data-version")
async def publish_data_version(
    r: redis.Redis = Depends(get_redis),
    _: None = Security(require_api_key),
):
    new_version = datetime.now(UTC).isoformat(timespec="seconds")

    await r.set(DATA_VERSION_KEY, new_version)

    return {
        "status": "published",
        "data_version": new_version,
        "message": "Redis data version updated successfully.",
    }


@router.get("/data-version")
async def get_data_version(
    r: redis.Redis = Depends(get_redis),
    _: None = Security(require_api_key),
):
    version = await r.get(DATA_VERSION_KEY)

    return {
        "data_version": version,
    }

@router.post("/clear_cache")
async def clear_cache(
    r: redis.Redis = Depends(get_redis),
    _: None = Security(require_api_key),
):
    await clear_redis_cache(r)

    return {"Message": "Redis cache cleared successfully."}


@router.get("/db_ping")
async def db_ping(
    conn: asyncpg.Connection = Depends(get_pg_conn),
    _: None = Security(require_api_key),
):
    value = await conn.fetchval("SELECT 1;")

    return {"OK": value == 1}


@router.get("/get_omni_event/{event_id}")
async def get_omni_event(
    event_id: int = Path(..., ge=1),
    client: httpx.AsyncClient = Depends(get_http_client),
    conn: asyncpg.Connection = Depends(get_pg_conn),
    _: None = Security(require_api_key),
):
    data = await get_omni_local_event(client, event_id)

    mapped_event = oem.map_event(data.event)
    mapped_players = oem.map_players(data.players)
    mapped_standings = oem.map_standings(event_id, data.standings)
    mapped_participants = oem.map_participants(event_id, data.rounds)

    payload = OmniCrudPayload(
        event=mapped_event,
        players=mapped_players,
        standings=mapped_standings,
        participants=mapped_participants,
    )

    transaction_id = await event_transactions(conn, payload)

    return {"status": f"Ok for event: {transaction_id}"}