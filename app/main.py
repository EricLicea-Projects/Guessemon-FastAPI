import os, redis.asyncio as redis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.schemas import GuessResponse
from app.api.deps import get_redis
from app.cache.redis_cache import get_cached_pokemon, clear_redis_cache
from app.services.hints import compare_pokemon_data


# redis://127.0.0.1
# redis://red-cv1ai0ogph6c73atdshg:6379

REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.from_url(
        REDIS_URL,
        encoding="utf8",
        decode_responses=True
    )
    try:
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)

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



@app.get('/pokemon_of_day')
async def pokemon_of_day(r: redis.Redis = Depends(get_redis)):
    return await get_cached_pokemon(r, None)


@app.post('/guesses/{pokemon_id}', response_model = GuessResponse)
async def submit_guess(pokemon_id: int, r:redis.Redis = Depends(get_redis)) -> GuessResponse:
    formatted_guess = await get_cached_pokemon(r, pokemon_id)
    formatted_correct = await get_cached_pokemon(r, None)
    hints = compare_pokemon_data(formatted_guess, formatted_correct)
    return GuessResponse(
        correct=(formatted_guess.id == formatted_correct.id),
        hints=hints
    )


@app.post('/clear_cache')
async def clear_cache(r:redis.Redis = Depends(get_redis)):
    await clear_redis_cache(r)
    return {'Message': 'Redis cache cleared successfully.'}