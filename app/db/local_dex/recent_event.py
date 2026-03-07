import asyncpg
from app.schemas.local_dex_data import LocalEvent

async def get_recent_event(
        conn: asyncpg.Connection
)-> LocalEvent:
    query = """
        SELECT *
            FROM omni_event
            ORDER BY start_at DESC
            LIMIT 1
    """
    event = await conn.fetchrow(query)

    return LocalEvent(**dict(event))