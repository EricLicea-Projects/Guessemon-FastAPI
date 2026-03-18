import asyncpg

from app.db.local_dex.event_standings import get_event_standings
from app.db.local_dex.recent_event import get_recent_event
from app.db.local_dex.main_element_play_rates import get_main_element_play_rates

async def fetch_recent_standings(
        conn: asyncpg.Connection
):
    event = await get_recent_event(conn)
    standings = await get_event_standings(event.event_id, conn)
    main_element_play_rates = await get_main_element_play_rates(conn)

    if not standings or not main_element_play_rates:
        return []
    
    return {
        'event': event,
        'standings': standings,
        'main_element_play_rates':main_element_play_rates
    }