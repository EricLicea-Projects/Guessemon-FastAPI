import redis.asyncio as redis
from redis.exceptions import RedisError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.core.settings import settings
from app.db.postgres import init_pg_pool, close_pg_pool
from app.api.v1.game import router as game_router
from app.api.ops import router as ops_router


async def init_redis(app: FastAPI) -> None:
    r = redis.from_url(
        str(settings.REDIS_URL),
        encoding="utf8",
        decode_responses=True,
    )
    try:
        await r.ping()
    except RedisError as e:
        await r.aclose()
        raise RuntimeError(f"Redis is unavailable at {settings.REDIS_URL}") from e

    app.state.redis = r


async def init_postgres(app: FastAPI) -> None:
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    await init_pg_pool(app, dsn=str(settings.DATABASE_URL))

    try:
        async with app.state.pg_pool.acquire() as conn:
            await conn.fetchval("SELECT 1;")
    except Exception as e:
        await close_pg_pool(app)
        raise RuntimeError(f"Postgres is unavailable at {settings.DATABASE_URL}") from e


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = None
    app.state.pg_pool = None

    await init_redis(app)
    await init_postgres(app)

    try:
        yield
    finally:
        await close_pg_pool(app)
        if app.state.redis is not None:
            await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(game_router, prefix='/api/v1')
app.include_router(ops_router, prefix='/ops')

@app.get('/', include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')
