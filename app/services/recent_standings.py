import asyncpg

from app.db.local_dex.event_standings import get_event_standings
from app.db.local_dex.recent_event import get_recent_event

async def fetch_recent_standings(
        conn: asyncpg.Connection
):
    event = await get_recent_event(conn)
    rows = await get_event_standings(event.event_id, conn)

    if not rows:
        return []
    
    return {'event': event, 'standings': rows}