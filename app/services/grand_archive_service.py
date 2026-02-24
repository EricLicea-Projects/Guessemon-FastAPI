import httpx
from asyncio import gather

from app.clients import grand_archive_api as ga
from app.schemas.omni_event_data import OmniEventData

async def get_omni_local_event(
        client: httpx.AsyncClient,
        event_id: int,
)-> OmniEventData:
    event, players, standings, *rounds = await gather(
        ga.get_omni_event(client,event_id),
        ga.get_omni_event_players(client, event_id),
        ga.get_omni_event_standings(client, event_id),
        *[ga.get_omni_event_pairings(client, event_id, round) for round in range(1,4)],       
    )

    return {'event': event, 'players': players, 'standings': standings, 'rounds': rounds}