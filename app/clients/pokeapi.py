from typing import Literal, Any
import httpx

from app.clients.http_client import fetch_json

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
Endpoint = Literal["pokemon", "pokemon-species"]

async def fetch_resource(
    client: httpx.AsyncClient,
    endpoint: Endpoint,
    pokemon_id: int
) -> Any:
    url = f"{POKEAPI_BASE_URL}/{endpoint}/{pokemon_id}"
    return await fetch_json(
        client,
        url,
        service_name="PokeAPI",
        not_found_detail="Pokemon Not Found",
    )

async def get_pokemon(client: httpx.AsyncClient, pokemon_id: int) -> Any:
    return await fetch_resource(client, "pokemon", pokemon_id)

async def get_pokemon_species(client: httpx.AsyncClient, pokemon_id: int) -> Any:
    return await fetch_resource(client, "pokemon-species", pokemon_id)