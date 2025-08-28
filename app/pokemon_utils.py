from fastapi import HTTPException
from pokeapi import get_pokemon, get_pokemon_species
from pokemon_parser import format_pokemon_data
from app.schemas import PokemonData

async def fetch_formatted_pokemon_data(pokemon_identifier: int | str) -> PokemonData :
   
    try:
        raw_pokemon_data = await get_pokemon(pokemon_identifier)
        raw_species_data = await get_pokemon_species(pokemon_identifier)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

    combined_data = {**raw_pokemon_data, **raw_species_data}
    formatted_data = format_pokemon_data(combined_data)
    return formatted_data
