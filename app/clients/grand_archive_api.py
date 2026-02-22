import httpx
from typing import Any, Literal

from app.clients.http_client import fetch_json

GA_BASE_URL = "https://api.gatcg.com/omnidex/events"
Endpoint = Literal["", "players", "standings", "pairings"]

async def _fetch_resource(
    client: httpx.AsyncClient,
    event_id: int,
    endpoint: Endpoint = "",
    *,
    params: dict[str, Any] | None = None,
) -> Any:
    url = f"{GA_BASE_URL}/{event_id}" + (f"/{endpoint}" if endpoint else "")
    return await fetch_json(
        client,
        url,
        params=params,
        service_name="GrandArchiveAPI",
        not_found_detail="OmniEvent Not Found",
    )

async def get_omni_event(client: httpx.AsyncClient, event_id: int) -> Any:
    return await _fetch_resource(client, event_id)

async def get_omni_event_players(client: httpx.AsyncClient, event_id: int) -> Any:
    return await _fetch_resource(client, event_id, "players")

async def get_omni_event_standings(client: httpx.AsyncClient, event_id: int) -> Any:
    return await _fetch_resource(client, event_id, "standings")

async def get_omni_event_pairings(client: httpx.AsyncClient, event_id: int, round_num: int) -> Any:
    return await _fetch_resource(
        client,
        event_id,
        "pairings",
        params={"round": round_num},
    )
