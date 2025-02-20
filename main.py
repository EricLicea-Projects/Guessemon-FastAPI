from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, Dict

from pokemon_utils import fetch_formatted_pokemon_data
from pokemon_cache import get_cached_pokemon_of_day
from pokemon_comparison import compare_pokemon_data


class GuessResponse(BaseModel):
    correct: bool
    hints: Optional[Dict] = None

app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Welcome to Guessamon API'}


@app.get('/pokemon/{pokemon_id}')
async def guess_pokemon(pokemon_id: int):

    formatted_guess = await fetch_formatted_pokemon_data(pokemon_id)
    formatted_correct = await get_cached_pokemon_of_day()

    hints = compare_pokemon_data(formatted_guess, formatted_correct)

    return GuessResponse(correct=False, hints=hints)