import asyncpg
import json
from app.schemas.local_dex_data import ChampionStats

async def get_champion_stats(conn:asyncpg.Connection)->list[ChampionStats]:
    query = """
        WITH champion_stats AS (
            SELECT
                oes.champion_id,
                COUNT(*) AS appearances,
                SUM(oes.wins) AS total_wins,
                SUM(oes.losses) AS total_losses,
                SUM(oes.stalemates) AS total_stalemates
            FROM omni_event_standing oes
            JOIN omni_event oe ON oe.event_id = oes.event_id
            WHERE oe.start_at >= '2026-04-12 17:00:00-07'
            GROUP BY oes.champion_id
        ),

        total_appearances AS (
            SELECT SUM(appearances) AS total
            FROM champion_stats
        ),

        element_rankings AS (
            SELECT
                oes.champion_id,
                ce.element_name,
                oes.main_element_id,
                COUNT(*) AS element_count,
                ROW_NUMBER() OVER (
                    PARTITION BY oes.champion_id
                    ORDER BY COUNT(*) DESC
                ) AS element_rank
            FROM omni_event_standing oes
            JOIN omni_event oe ON oe.event_id = oes.event_id
            JOIN champion_element ce ON ce.element_id = oes.main_element_id
            WHERE oe.start_at >= '2026-04-12 17:00:00-07'
            GROUP BY oes.champion_id, oes.main_element_id, ce.element_name
        ),

        top_3_elements AS (
            SELECT
                champion_id,
                JSON_AGG(
                    JSON_BUILD_OBJECT('element_id',main_element_id,'element_name',element_name) 
                    ORDER BY element_rank
                ) AS top_elements
            FROM element_rankings
            WHERE element_rank <= 3
            GROUP BY champion_id
        )

        SELECT
            cs.champion_id,
            c.champion_name,
            ROUND(cs.appearances::NUMERIC / ta.total * 100, 2) AS pick_rate,
            ROUND(
                cs.total_wins::NUMERIC
                / NULLIF(cs.total_wins + cs.total_losses + cs.total_stalemates, 0) * 100, 2
            ) AS win_rate,
            te.top_elements
        FROM champion_stats cs
        JOIN champion c ON c.champion_id = cs.champion_id
        CROSS JOIN total_appearances ta
        JOIN top_3_elements te ON te.champion_id = cs.champion_id
        ORDER BY cs.appearances DESC;
    """

    rows = await conn.fetch(query)

    return [
        ChampionStats(**{**row, "top_elements": json.loads(row["top_elements"])})
        for row in rows
    ]