import json
import redis.asyncio as redis
from datetime import datetime, timedelta, timezone, time

from app.services import fetch_formatted_pokemon_data, pokemon_of_day
from app.schemas import PokemonData


async def clear_redis_cache(client: redis.Redis) -> None:
    await client.flushall()


async def get_cached_pokemon(client: redis.Redis, pokemon_id: int | None) -> PokemonData:
    day_key = datetime.now(timezone.utc).date().isoformat()
    
    is_default = False
    if pokemon_id is None:
        pokemon_id = pokemon_of_day()
        is_default = True

    cache_key = f"pokemon_of_day:{day_key}" if is_default else f"pokemon:{pokemon_id}:{day_key}"
    
    cached = await client.get(cache_key)
    if cached:
        print('Cache Hit')
        return PokemonData(**json.loads(cached))
    
    formatted_data = await fetch_formatted_pokemon_data(pokemon_id)
    
    # Expire at UTC midnight
    now = datetime.now(timezone.utc)
    expires_at = datetime.combine(now.date() + timedelta(days=1), time(0, 0, tzinfo = timezone.utc))
    ttl = max(1, int((expires_at - now).total_seconds()))
    
    await client.set(cache_key, json.dumps(formatted_data.model_dump()), ex=ttl)
    return formatted_data
