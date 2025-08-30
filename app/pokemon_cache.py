import json
import random
from datetime import datetime, timedelta
from typing import Optional
import redis.asyncio as redis

from app.services.pokemon_service import fetch_formatted_pokemon_data
from app.schemas import PokemonData

redis_client = None

# redis://127.0.0.1
# redis://red-cv1ai0ogph6c73atdshg:6379

async def get_redis_client() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url("redis://127.0.0.1", encoding="utf8", decode_responses=True)
    return redis_client

async def clear_redis_cache() -> None:
    client = await get_redis_client()
    await client.flushall()


def get_pokemon_of_the_day() -> int:
    seed_value = int(datetime.now().strftime('%Y%j'))
    random.seed(seed_value)
    return random.randint(1, 1025)

async def get_cached_pokemon(pokemon_id: Optional[int] = None) -> PokemonData:
    client = await get_redis_client()
    day_key = datetime.now().strftime("%Y-%m-%d")
    
    is_default = False
    if pokemon_id is None:
        pokemon_id = get_pokemon_of_the_day()
        is_default = True

    cache_key = f"pokemon_of_day:{day_key}" if is_default else f"pokemon:{pokemon_id}:{day_key}"
    
    cached = await client.get(cache_key)
    if cached:
        print('Cache Hit')
        cached_dict = json.loads(cached)
        return PokemonData(**cached_dict)
    
    formatted_data = await fetch_formatted_pokemon_data(pokemon_id)
    
    now = datetime.now()
    tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    ttl = int((tomorrow - now).total_seconds())
    
    await client.set(cache_key, json.dumps(formatted_data.model_dump()), ex=ttl)
    return formatted_data
