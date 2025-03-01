from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict

from pokemon_utils import fetch_formatted_pokemon_data
from pokemon_cache import get_cached_pokemon_of_day
from pokemon_comparison import compare_pokemon_data


class GuessResponse(BaseModel):
    correct: bool
    hints: Optional[Dict] = None

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://guessemon.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def read_root():
    return {'message': 'Welcome to Guessamon API'}


@app.get('/pokemon/{pokemon_id}')
async def guess_pokemon(pokemon_id: int):
    formatted_guess = await fetch_formatted_pokemon_data(pokemon_id)
    formatted_correct = await get_cached_pokemon_of_day()
    hints = compare_pokemon_data(formatted_guess, formatted_correct)

    if formatted_guess.id == formatted_correct.id:
        return GuessResponse(correct=True, hints=hints)
    else:
        return GuessResponse(correct=False, hints=hints)