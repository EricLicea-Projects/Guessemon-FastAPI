from asyncio import gather
from app.schemas import PokemonData
from app.clients import get_pokemon, get_pokemon_species
from app.mappers.pokemon import to_pokemon_data

async def fetch_formatted_pokemon_data(pokemon_id: int) -> PokemonData :
    """Fetches /pokemon and /pokemon-species concurrently, merges them,
    and returns a formatted PokemonData schema."""
   
    raw_pokemon, raw_species = await gather(
        get_pokemon(pokemon_id),
        get_pokemon_species(pokemon_id),
    )

    combined_data = {**raw_pokemon, **raw_species}
    return to_pokemon_data(combined_data)