import json

import redis.asyncio as redis
from fastapi import APIRouter, Depends

from app.api.deps import get_redis
from app.cache.keys import MAINTENANCE_KEY

router = APIRouter(tags=["status"])


@router.get("/status")
async def get_status(
    r: redis.Redis = Depends(get_redis),
):
    raw = await r.get(MAINTENANCE_KEY)

    if raw is None:
        return {
            "ok": True,
            "maintenance": False,
            "message": None,
        }

    data = json.loads(raw)

    maintenance_enabled = data.get("enabled", False)

    return {
        "ok": not maintenance_enabled,
        "maintenance": maintenance_enabled,
        "message": data.get("message"),
    }