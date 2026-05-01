import json
import httpx
from fastapi.encoders import jsonable_encoder

import redis.asyncio as redis
from datetime import datetime, timedelta, timezone, time
from collections.abc import Awaitable, Callable
from typing import TypeVar

from app.services import fetch_formatted_pokemon_data, pokemon_of_day
from app.schemas import PokemonData
from app.cache.keys import DATA_VERSION_KEY

T = TypeVar("T")

CACHE_NAMESPACE = "guessamon"
DEFAULT_CACHE_TTL_SECONDS = 4 * 24 * 60 * 60



async def clear_redis_cache(r: redis.Redis) -> None:
    await r.flushall()


async def get_cached_pokemon(
        r: redis.Redis,
        client: httpx.AsyncClient,
        pokemon_id: int | None,
) -> PokemonData:
    day_key = datetime.now(timezone.utc).date().isoformat()
    
    is_default = False
    if pokemon_id is None:
        pokemon_id = pokemon_of_day()
        is_default = True

    cache_key = f"pokemon_of_day:{day_key}" if is_default else f"pokemon:{pokemon_id}:{day_key}"
    
    cached = await r.get(cache_key)
    if cached:
        print('Cache Hit')
        return PokemonData(**json.loads(cached))
    
    formatted_data = await fetch_formatted_pokemon_data(client, pokemon_id)
    
    # Expire at UTC midnight
    now = datetime.now(timezone.utc)
    expires_at = datetime.combine(now.date() + timedelta(days=1), time(0, 0, tzinfo = timezone.utc))
    ttl = max(1, int((expires_at - now).total_seconds()))
    
    await r.set(cache_key, json.dumps(formatted_data.model_dump()), ex=ttl)
    return formatted_data


async def get_data_version(r: redis.Redis) -> str:
    version = await r.get(DATA_VERSION_KEY)

    if version is None:
        version = "dev"
        await r.set(DATA_VERSION_KEY, version)

    return str(version)


def make_cache_key(version: str, resource: str, *parts: object) -> str:
    extra_parts = ":".join(str(part) for part in parts)

    if extra_parts:
        return f"{CACHE_NAMESPACE}:api:v{version}:{resource}:{extra_parts}"

    return f"{CACHE_NAMESPACE}:api:v{version}:{resource}"


async def get_or_set_json(
    r: redis.Redis,
    key: str,
    fetcher: Callable[[], Awaitable[T]],
    ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
):
    cached = await r.get(key)

    if cached is not None:
        print(f"Cache HIT: {key}")
        return json.loads(cached)

    print(f"Cache MISS: {key}")

    data = await fetcher()

    encoded_data = jsonable_encoder(data)

    await r.set(
        key,
        json.dumps(encoded_data),
        ex=ttl_seconds,
    )

    return encoded_data