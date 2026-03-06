import asyncpg
from app.schemas.omni_event_data import OmniCrudPayload
from app.db.omni_event.event_crud import event_crud
from app.db.omni_event.player_crud import player_crud
from app.db.omni_event.event_player_crud import event_player_crud
from app.db.omni_event.event_judge_crud import event_judge_crud
from app.db.omni_event.standing_crud import standing_crud
from app.db.omni_event.participant_crud import participant_crud



async def event_transactions(conn:asyncpg.Connection, payload: OmniCrudPayload):
    players = payload.event.players
    judges = payload.event.judges
    async with conn.transaction():
        event_id = await event_crud(conn, payload.event)
        await player_crud(conn, payload.players)
        await event_player_crud(conn, event_id, players)
        await event_judge_crud(conn, event_id, judges)
        await standing_crud(conn, payload.standings)
        await participant_crud(conn, payload.participants)
    
    return event_id