from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel

from pokeapi import get_pokemon, get_pokemon_species
from pokemon_parser import format_pokemon_data


app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Welcome to Guessamon API'}

@app.get('/pokemon/{pokemon_name}')
async def fetch_pokemon(pokemon_name: str):
    
    try:
        raw_pokemon_data = await get_pokemon(pokemon_name)
        raw_species_data = await get_pokemon_species(pokemon_name)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    
    combined_data = {
        **raw_pokemon_data,
        **raw_species_data,
    }

    formatted_data = format_pokemon_data(combined_data)

    return formatted_data.model_dump()