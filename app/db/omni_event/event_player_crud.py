import asyncpg
from typing import Sequence
from app.db.omni_event.upsert_event_people_join import upsert_event_people_join

async def event_player_crud(conn: asyncpg.Connection, event_id: int, players: Sequence[int]) -> None:
    await upsert_event_people_join(conn, "omni_event_player", event_id, players)