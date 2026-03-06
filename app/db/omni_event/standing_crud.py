import asyncpg
from typing import Sequence
from app.schemas.omni_event_data import OmniEventStanding

async def standing_crud(
    conn: asyncpg.Connection,
    standings: Sequence[OmniEventStanding],
) -> None:
    if not standings:
        raise ValueError("standing_crud received an empty standings list")

    query = """
        INSERT INTO omni_event_standing (
            event_id,
            player_id,
            placement,
            wins,
            losses,
            stalemates,
            byes,
            score
        )
        SELECT
            t.event_id,
            t.player_id,
            t.placement,
            t.wins,
            t.losses,
            t.stalemates,
            t.byes,
            t.score
        FROM unnest(
            $1::int[],
            $2::int[],
            $3::int[],
            $4::int[],
            $5::int[],
            $6::int[],
            $7::int[],
            $8::int[]
        ) AS t(
            event_id,
            player_id,
            placement,
            wins,
            losses,
            stalemates,
            byes,
            score
        )
        ON CONFLICT (event_id, player_id) DO UPDATE SET
            placement  = EXCLUDED.placement,
            wins       = EXCLUDED.wins,
            losses     = EXCLUDED.losses,
            stalemates = EXCLUDED.stalemates,
            byes       = EXCLUDED.byes,
            score      = EXCLUDED.score;
    """

    event_ids   = [s.event_id for s in standings]
    player_ids  = [s.player_id for s in standings]
    placements  = [s.placement for s in standings]
    wins        = [s.wins for s in standings]
    losses      = [s.losses for s in standings]
    stalemates  = [s.stalemates for s in standings]
    byes        = [s.byes for s in standings]
    scores      = [s.score for s in standings]

    await conn.execute(
        query,
        event_ids,
        player_ids,
        placements,
        wins,
        losses,
        stalemates,
        byes,
        scores,
    )