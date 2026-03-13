import asyncpg
from app.schemas.local_dex_data import LocalStanding

async def get_event_standings(
        event_id: int,
        conn: asyncpg.Connection
)->list[LocalStanding]:
    query = """
        SELECT 
            s.placement,
            p.username,
            s.player_id,
            s.wins,
            s.losses,
            s.stalemates,
            s.byes,
            s.score,
            s.main_element_id,
            s.champion_id,
            ce.element_name        AS main_element,
            ch_el.element_name     AS champion_element,
            ch.champion_name,
            cc.class_name          AS champion_class,
            sc.class_name          AS champion_sub_class
        FROM omni_event_standing s
        JOIN omni_player p ON p.player_id = s.player_id
        JOIN champion_element ce  ON ce.element_id  = s.main_element_id
        JOIN champion ch          ON ch.champion_id = s.champion_id
        JOIN champion_element ch_el ON ch_el.element_id = ch.element_id
        JOIN champion_class cc    ON cc.class_id    = ch.class_id
        LEFT JOIN champion_class sc ON sc.class_id  = ch.sub_class_id
        WHERE event_id = $1
        ORDER BY placement ASC;
    """
    rows = await conn.fetch(query, event_id)

    return [LocalStanding(**dict(row)) for row in rows]
