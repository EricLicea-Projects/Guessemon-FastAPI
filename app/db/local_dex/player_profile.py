import asyncpg
import json

async def player_profile(conn: asyncpg.Connection, player_id: int):
    query = """
        WITH player_base AS (
            SELECT
                player_id,
                username,
                player_cp,
                player_rank,
                player_emblem
            FROM omni_player
            WHERE player_id = $1
        ),
        season_standings AS (
            SELECT
                oes.*,
                oe.start_at
            FROM omni_event_standing oes
            JOIN omni_event oe ON oe.event_id = oes.event_id
            WHERE oes.player_id = $1
            AND oe.start_at >= '2026-04-12 17:00:00-07'
        ),
        overall_stats AS (
            SELECT
                SUM(wins) AS total_wins,
                SUM(losses) AS total_losses,
                SUM(wins) + SUM(losses) AS total_games,
                ROUND(
                    100.0 * SUM(wins) / NULLIF(SUM(wins) + SUM(losses), 0),
                    2
                ) AS win_rate,
                (
                    SELECT ce.element_name
                    FROM season_standings ss2
                    JOIN champion_element ce ON ce.element_id = ss2.main_element_id
                    GROUP BY ce.element_name
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                ) AS most_played_element
            FROM season_standings
        ),
        champion_mastery AS (
            SELECT
                ch.champion_id,
                ch.champion_name,
                COUNT(*) AS events_played,
                SUM(ss.wins) AS wins,
                SUM(ss.losses) AS losses,
                ROUND(
                    100.0 * SUM(ss.wins) / NULLIF(SUM(ss.wins) + SUM(ss.losses), 0),
                    2
                ) AS win_rate
            FROM season_standings ss
            JOIN champion ch ON ch.champion_id = ss.champion_id
            GROUP BY ch.champion_id, ch.champion_name
            ORDER BY events_played DESC
        ),
        advanced_element_usage AS (
            SELECT
                ce.element_name,
                COUNT(*) AS times_played
            FROM season_standings ss
            JOIN champion ch ON ch.champion_id = ss.champion_id
            JOIN champion_element ce ON ce.element_id = ch.element_id
            WHERE ch.element_id >= 5
            GROUP BY ce.element_name
            ORDER BY times_played DESC
        ),
        event_history AS (
            SELECT
                oe.event_id,
                oe.start_at,
                ss.placement,
                ss.wins,
                ss.losses,
                ss.stalemates,
                ch.champion_name,
                ch_el.element_name AS champion_element,
                main_el.element_name AS main_element
            FROM season_standings ss
            JOIN omni_event oe ON oe.event_id = ss.event_id
            JOIN champion ch ON ch.champion_id = ss.champion_id
            JOIN champion_element ch_el ON ch_el.element_id = ch.element_id
            JOIN champion_element main_el ON main_el.element_id = ss.main_element_id
            ORDER BY oe.start_at DESC
        )
        SELECT
            pb.*,
            os.*,
            COALESCE((SELECT json_agg(champion_mastery) FROM champion_mastery), '[]') AS champion_mastery,
            COALESCE((SELECT json_agg(advanced_element_usage) FROM advanced_element_usage), '[]') AS advanced_element_usage,
            COALESCE((SELECT json_agg(event_history) FROM event_history), '[]') AS event_history
        FROM player_base pb, overall_stats os;
    """

    row = await conn.fetchrow(query, player_id)

    if not row:
        return None
    
    row = dict(row)

    row['champion_mastery'] = json.loads(row['champion_mastery'])
    row['advanced_element_usage'] = json.loads(row['advanced_element_usage'])
    row['event_history'] = json.loads(row['event_history'])
    
    return row