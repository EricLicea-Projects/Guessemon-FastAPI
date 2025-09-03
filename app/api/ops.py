import redis.asyncio as redis
from fastapi import APIRouter, Security, Depends

from app.api.deps import get_redis
from app.core.security import require_api_key
from app.cache.redis_cache import clear_redis_cache

router = APIRouter(tags = ['ops'])

@router.post('/clear_cache')
async def clear_cache(r:redis.Redis = Depends(get_redis), _: None = Security(require_api_key)):
    await clear_redis_cache(r)
    return {'Message': 'Redis cache cleared successfully.'}