import asyncpg
from app.schemas.local_dex_data import LocalStanding

async def get_event_standings(
        event_id: int,
        conn: asyncpg.Connection
)->list[LocalStanding]:
    query = """
        SELECT
            s.placement,
            p.username,
            s.player_id,
            s.wins,
            s.losses,
            s.stalemates,
            s.byes,
            s.score
        FROM omni_event_standing s
        JOIN omni_player p ON s.player_id = p.player_id
        WHERE s.event_id = $1
        ORDER BY s.placement ASC;
    """
    rows = await conn.fetch(query, event_id)

    return [LocalStanding(**dict(row)) for row in rows]
