import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.settings import settings
from app.api.v1.game import router as game_router
from app.api.ops import router as ops_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.from_url(
        str(settings.REDIS_URL),
        encoding="utf8",
        decode_responses=True
    )
    try:
        yield
    finally:
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
