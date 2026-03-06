import asyncpg
from typing import Sequence
from app.db.omni_event.upsert_event_people_join import upsert_event_people_join

async def event_judge_crud(conn: asyncpg.Connection, event_id: int, judges: Sequence[int]) -> None:
    await upsert_event_people_join(conn, "omni_event_judge", event_id, judges)