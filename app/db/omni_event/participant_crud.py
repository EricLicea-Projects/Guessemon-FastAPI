import asyncpg
from typing import Sequence
from app.schemas.omni_event_data import OmniEventParticipant

async def participant_crud(
    conn: asyncpg.Connection,
    participants: Sequence[OmniEventParticipant],
) -> None:
    if not participants:
        raise ValueError("participant_crud received an empty participants list")

    query = """
        INSERT INTO omni_match_participant (
            event_id,
            player_id,
            round_id,
            pairing_id,
            dropped,
            score,
            status,
            elo_change
        )
        SELECT
            t.event_id,
            t.player_id,
            t.round_id,
            t.pairing_id,
            t.dropped,
            t.score,
            t.status,
            t.elo_change
        FROM unnest(
            $1::int[],
            $2::int[],
            $3::int[],
            $4::int[],
            $5::boolean[],
            $6::int[],
            $7::text[],
            $8::numeric[]
        ) AS t(
            event_id,
            player_id,
            round_id,
            pairing_id,
            dropped,
            score,
            status,
            elo_change
        )
        ON CONFLICT (event_id, player_id, round_id, pairing_id) DO UPDATE SET
            dropped    = EXCLUDED.dropped,
            score      = EXCLUDED.score,
            status     = EXCLUDED.status,
            elo_change = EXCLUDED.elo_change;
    """

    event_ids   = [p.event_id for p in participants]
    player_ids  = [p.player_id for p in participants]
    round_ids   = [p.round_id for p in participants]
    pairing_ids = [p.pairing_id for p in participants]
    dropped     = [p.dropped for p in participants]
    scores      = [p.score for p in participants]
    statuses    = [p.status for p in participants]
    elo_changes = [p.elo_change for p in participants]

    await conn.execute(
        query,
        event_ids,
        player_ids,
        round_ids,
        pairing_ids,
        dropped,
        scores,
        statuses,
        elo_changes,
    )