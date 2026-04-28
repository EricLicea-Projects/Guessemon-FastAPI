from fastapi import APIRouter, Depends
import asyncpg

from app.api.deps import get_pg_conn
from app.services.recent_standings import fetch_recent_standings
from app.db.local_dex.get_player_stats import get_player_stats
from app.db.local_dex.player_profile import player_profile

router = APIRouter(tags=['LocalDex'])

@router.get('/standings')
async def get_recent_standings(
        conn: asyncpg.Connection = Depends(get_pg_conn)
):
    return await fetch_recent_standings(conn)


@router.get('/player-stats')
async def get_player_stats_table(
        conn: asyncpg.Connection = Depends(get_pg_conn)
):
    return await get_player_stats(conn)


@router.get('/player-profile/{player_id}')
async def get_player_profile(
        player_id: int,
        conn: asyncpg.Connection = Depends(get_pg_conn)
):
    return await player_profile(conn, player_id)