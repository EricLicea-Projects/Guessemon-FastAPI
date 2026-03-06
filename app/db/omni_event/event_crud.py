import asyncpg
from app.schemas.omni_event_data import OmniEvent

async def event_crud(conn: asyncpg.Connection, event: OmniEvent) -> int:
    query = """
        INSERT INTO omni_event (
            event_id, ranked, swiss_match_config, swiss_rounds, start_at, url
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (event_id) 
        DO UPDATE SET
            ranked = EXCLUDED.ranked,
            swiss_match_config = EXCLUDED.swiss_match_config,
            swiss_rounds = EXCLUDED.swiss_rounds,
            start_at = EXCLUDED.start_at,
            url = EXCLUDED.url
        RETURNING event_id;
    """
    
    event_id = await conn.fetchval(
        query,
        event.event_id,
        event.ranked,
        event.swiss_match_config,
        event.swiss_rounds,
        event.start_at,
        event.url
    )
    
    return event_id