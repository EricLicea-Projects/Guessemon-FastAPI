from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict

from pokemon_cache import get_cached_pokemon,  clear_redis_cache
from pokemon_comparison import compare_pokemon_data



class GuessResponse(BaseModel):
    correct: bool
    hints: Optional[Dict] = None

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://guessemon.vercel.app",
    "https://guessamon.xyz",
    "https://www.guessamon.xyz"
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


@app.post("/clear_cache")
async def clear_cache_endpoint():
    try:
        await clear_redis_cache()
        return {"message": "Redis cache cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/pokemon_of_day')
async def pokemon_of_day():
    return await get_cached_pokemon()
    

@app.get('/pokemon/{pokemon_id}')
async def guess_pokemon(pokemon_id: int):
    formatted_guess = await get_cached_pokemon(pokemon_id)
    formatted_correct = await get_cached_pokemon()
    hints = compare_pokemon_data(formatted_guess, formatted_correct)

    if formatted_guess.id == formatted_correct.id:
        return GuessResponse(correct=True, hints=hints)
    else:
        return GuessResponse(correct=False, hints=hints)