import asyncpg
from typing import List
from app.schemas.omni_event_data import OmniPlayer

async def player_crud(conn: asyncpg.Connection, players: List[OmniPlayer]) -> None:
    query = """
        INSERT INTO omni_player (
            player_id, username, country, player_cp, player_rank, player_emblem
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (player_id)
        DO UPDATE SET
            username = EXCLUDED.username,
            country = EXCLUDED.country,
            player_cp = EXCLUDED.player_cp,
            player_rank = EXCLUDED.player_rank,
            player_emblem = EXCLUDED.player_emblem;
    """
    
    data = [
        (p.player_id, p.username, p.country, p.player_cp, p.player_rank, p.player_emblem)
        for p in players
    ]
    
    await conn.executemany(query, data)