import asyncpg
import json
from app.schemas.local_dex_data import PlayerStats

async def get_player_stats(conn: asyncpg.Connection) -> list[PlayerStats]:
    query = """
        WITH season_standings AS (
            SELECT
                oes.*
            FROM omni_event_standing oes
            JOIN omni_event oe ON oe.event_id = oes.event_id
            WHERE oe.start_at >= '2026-04-12 17:00:00-07'
            AND oe.ranked = true
        ),
        player_stats AS (
            SELECT
                player_id,
                SUM(COALESCE(wins, 0) + COALESCE(losses, 0) + COALESCE(stalemates, 0)) AS games_played,
                ROUND(
                    100.0 * SUM(COALESCE(wins, 0))::numeric
                    / NULLIF(
                        SUM(COALESCE(wins, 0) + COALESCE(losses, 0) + COALESCE(stalemates, 0)),
                        0
                    ),
                    2
                ) AS win_rate
            FROM season_standings
            GROUP BY player_id
        ),
        ranked_elements AS (
            SELECT
                player_id,
                main_element_id,
                COUNT(DISTINCT event_id) AS times_used,
                ROW_NUMBER() OVER (
                    PARTITION BY player_id
                    ORDER BY COUNT(DISTINCT event_id) DESC, main_element_id  -- tiebreak
                ) AS element_rank
            FROM season_standings
            GROUP BY player_id, main_element_id
        ),
        ranked_champions AS (
            SELECT
                player_id,
                champion_id,
                COUNT(DISTINCT event_id) AS times_played,
                ROW_NUMBER() OVER (
                    PARTITION BY player_id
                    ORDER BY COUNT(DISTINCT event_id) DESC, champion_id  -- tiebreak
                ) AS champion_rank
            FROM season_standings
            WHERE champion_id IS NOT NULL
            GROUP BY player_id, champion_id
        ),
        top_champions AS (
            SELECT
                rc.player_id,
                jsonb_agg(
                    jsonb_build_object(
                        'champion_id', rc.champion_id,
                        'champion_name', c.champion_name,
                        'times_played', rc.times_played
                    )
                    ORDER BY rc.champion_rank
                ) AS champions
            FROM ranked_champions rc
            LEFT JOIN champion c ON c.champion_id = rc.champion_id
            WHERE rc.champion_rank <= 3
            GROUP BY rc.player_id
        )
        SELECT
            ps.player_id,
            op.username,
            op.player_cp,
            ps.games_played,
            ps.win_rate,
            re.main_element_id,
            ce.element_name AS main_element,
            COALESCE(tc.champions, '[]'::jsonb) AS top_3_champions
        FROM player_stats ps
        LEFT JOIN omni_player op        ON op.player_id = ps.player_id
        LEFT JOIN ranked_elements re    ON re.player_id = ps.player_id AND re.element_rank = 1
        LEFT JOIN champion_element ce   ON ce.element_id = re.main_element_id
        LEFT JOIN top_champions tc      ON tc.player_id = ps.player_id
        ORDER BY op.player_cp DESC;
        """
    rows = await conn.fetch(query)

    player_stats: list[PlayerStats] = []

    for row in rows:
        data = dict(row)

        if isinstance(data["top_3_champions"], str):
            data["top_3_champions"] = json.loads(data["top_3_champions"])

        player_stats.append(PlayerStats.model_validate(data))

    return player_stats