import httpx
from fastapi import HTTPException

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

async def fetch_resource(endpoint: str, pokemon_id: int) -> dict:
    url = f"{POKEAPI_BASE_URL}/{endpoint}/{pokemon_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Pokemon Not Found")
        return response.json()

async def get_pokemon(pokemon_id: int) -> dict:
    return await fetch_resource("pokemon", pokemon_id)

async def get_pokemon_species(pokemon_id: int) -> dict:
    return await fetch_resource("pokemon-species", pokemon_id)
