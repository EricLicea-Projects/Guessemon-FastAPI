import asyncpg
from typing import Sequence, Literal

JoinTable = Literal["omni_event_player", "omni_event_judge"]

async def upsert_event_people_join(
    conn: asyncpg.Connection,
    table: JoinTable,
    event_id: int,
    person_ids: Sequence[int],
) -> None:
    if not person_ids:
        raise ValueError(f"{table} upsert received an empty id list")

    query = f"""
        INSERT INTO {table} (event_id, player_id)
        SELECT $1, p.player_id
        FROM (
            SELECT DISTINCT unnest($2::int[]) AS player_id
        ) AS p
        ON CONFLICT (event_id, player_id) DO NOTHING;
    """
    await conn.execute(query, event_id, list(person_ids))