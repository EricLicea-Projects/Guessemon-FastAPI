from fastapi import APIRouter, Depends
import redis.asyncio as redis

from app.api.deps import get_redis
from app.cache.redis_cache import get_cached_pokemon
from app.schemas import GuessResponse, PokemonData
from app.services.hints import compare_pokemon_data

router = APIRouter(tags=['game'])

@router.get('/pokemon_of_day', response_model=PokemonData)
async def pokemon_of_day(r: redis.Redis = Depends(get_redis)):
    return await get_cached_pokemon(r, None)


@router.post('/guesses/{pokemon_id}', response_model = GuessResponse)
async def submit_guess(pokemon_id: int, r:redis.Redis = Depends(get_redis)) -> GuessResponse:
    formatted_guess = await get_cached_pokemon(r, pokemon_id)
    formatted_correct = await get_cached_pokemon(r, None)
    hints = compare_pokemon_data(formatted_guess, formatted_correct)
    return GuessResponse(correct=(formatted_guess.id == formatted_correct.id), hints=hints)