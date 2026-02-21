import httpx
from asyncio import gather
from app.schemas import PokemonData
from app.clients import get_pokemon, get_pokemon_species
from app.mappers.pokemon import to_pokemon_data

async def fetch_formatted_pokemon_data(
        client: httpx.AsyncClient,
        pokemon_id: int,
) -> PokemonData :
    """Fetches /pokemon and /pokemon-species concurrently, merges them,
    and returns a formatted PokemonData schema."""
   
    raw_pokemon, raw_species = await gather(
        get_pokemon(client, pokemon_id),
        get_pokemon_species(client, pokemon_id),
    )

    combined_data = {**raw_pokemon, **raw_species}
    return to_pokemon_data(combined_data)