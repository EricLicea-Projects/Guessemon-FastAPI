import asyncpg
from app.schemas.local_dex_data import MainElementPlayRate

async def get_main_element_play_rates(
        conn: asyncpg.Connection
)->list[MainElementPlayRate]:
    query ="""
        SELECT
            ce.element_name,
            COUNT(oes.main_element_id) AS times_played,
            ROUND(
                100.0 * COUNT(oes.main_element_id) / SUM(COUNT(oes.main_element_id)) OVER (),
                2
            ) AS play_rate
        FROM champion_element ce
        LEFT JOIN omni_event_standing oes ON ce.element_id = oes.main_element_id
        LEFT JOIN omni_event oe ON oe.event_id = oes.event_id
        WHERE ce.element_id BETWEEN 1 AND 4
        AND (oe.start_at >= '2026-04-12 17:00:00-07' OR oe.start_at IS NULL)
        GROUP BY ce.element_name
        ORDER BY play_rate DESC;
    """
    rows = await conn.fetch(query)

    return [MainElementPlayRate(**dict(row)) for row in rows]