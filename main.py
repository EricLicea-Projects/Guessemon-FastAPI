from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel

from pokeapi import get_pokemon


app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Welcome to Guessamon API'}

@app.get('/pokemon/{pokemon_name}')
async def fetch_pokemon(pokemon_name: str):
    pokemon_data = await get_pokemon(pokemon_name)
    return pokemon_data