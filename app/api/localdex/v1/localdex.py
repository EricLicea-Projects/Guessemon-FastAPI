from fastapi import APIRouter, Depends
import asyncpg

from app.api.deps import get_pg_conn
from app.services.recent_standings import fetch_recent_standings

router = APIRouter(tags=['LocalDex'])

@router.get('/standings')
async def get_recent_standings(
        conn: asyncpg.Connection = Depends(get_pg_conn)
):
    return await fetch_recent_standings(conn)