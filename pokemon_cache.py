import json
from datetime import datetime, timedelta
import redis.asyncio as redis

from pokemon_of_the_day import get_pokemon_of_the_day
from pokemon_utils import fetch_formatted_pokemon_data

redis_client = None

async def get_redis_client() -> redis.Redis:

    global redis_client
    if redis_client is None:
        redis_client = redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    return redis_client

async def get_cached_pokemon_of_day() -> dict:

    client = await get_redis_client()
    day_key = datetime.now().strftime("%Y-%m-%d")
    cache_key = f"pokemon_of_day:{day_key}"
    
    cached = await client.get(cache_key)
    if cached:
        print('Cash Hit')
        return json.loads(cached)
    
    pokemon_id = get_pokemon_of_the_day()
    formatted_data = await fetch_formatted_pokemon_data(pokemon_id)
    
    now = datetime.now()
    tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    ttl = int((tomorrow - now).total_seconds())
    
    await client.set(cache_key, json.dumps(formatted_data.model_dump()), ex=ttl)
    return formatted_data.model_dump()
