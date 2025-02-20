from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, Dict

from pokemon_of_the_day import get_pokemon_of_the_day
from pokemon_utils import fetch_formatted_pokemon_data
from pokemon_cache import get_cached_pokemon_of_day


class GuessResponse(BaseModel):
    correct: bool
    hints: Optional[Dict] = None

app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Welcome to Guessamon API'}

# Test Endpoint to make sure pokemon of the day is working.
@app.get('/pokemon_of_day')
async def pokemon_of_today():
    return get_pokemon_of_the_day()


@app.get('/pokemon/{pokemon_id}')
async def guess_pokemon(pokemon_id: int):
    pokemon_of_day_id = get_pokemon_of_the_day()

    if pokemon_of_day_id == pokemon_id:
        return GuessResponse(correct=True)
    
    formatted_guess = await fetch_formatted_pokemon_data(pokemon_id)
    formatted_correct = await get_cached_pokemon_of_day()
    print(formatted_correct)

    return GuessResponse(correct=False)