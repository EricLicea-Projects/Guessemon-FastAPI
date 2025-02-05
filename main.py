from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel

from pokeapi import get_pokemon
from pokemon_parser import format_pokemon_data


app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Welcome to Guessamon API'}

@app.get('/pokemon/{pokemon_name}')
async def fetch_pokemon(pokemon_name: str):
    pokemon_data = await get_pokemon(pokemon_name)
    if not pokemon_data:
        raise HTTPException(status_code=404, detail='Pokemon Not Found')
    
    formated_data = format_pokemon_data(pokemon_data)
    
    return formated_data.model_dump()