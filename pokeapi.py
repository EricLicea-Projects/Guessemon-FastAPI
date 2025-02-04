import httpx
from fastapi import HTTPException

POKEAPI_BASE_URL = 'https://pokeapi.co/api/v2'

async def get_pokemon(pokemon_name: str) -> dict:

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name.lower()}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail='Pokemon Not Found')
        return response.json()