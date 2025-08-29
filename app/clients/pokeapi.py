import httpx
from typing import Literal
from fastapi import HTTPException

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
DEFAULT_TIMEOUT = httpx.Timeout(10.0)

Endpoint = Literal['pokemon', 'pokemon-species']

async def fetch_resource(endpoint: Endpoint, pokemon_id: int) -> dict:
    url = f"{POKEAPI_BASE_URL}/{endpoint}/{pokemon_id}"
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)
    except httpx.RequestError as e:
        raise HTTPException(status_code = 502, detail = f'PokeAPI network error: {e}')from e

    if response.status_code == 404:
        raise HTTPException(status_code = 404, detail="Pokemon Not Found")
    
    if response.status_code >= 400:
        raise HTTPException(status_code = 502, detail=f'PokeAPI error {response.status_code}')
    
    return response.json()

async def get_pokemon(pokemon_id: int) -> dict:
    return await fetch_resource("pokemon", pokemon_id)

async def get_pokemon_species(pokemon_id: int) -> dict:
    return await fetch_resource("pokemon-species", pokemon_id)
