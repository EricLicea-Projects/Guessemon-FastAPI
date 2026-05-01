from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.settings import settings
from app.core.lifespan import lifespan
from app.core.middleware import maintenance_middleware
from app.api.guessamon.v1.game import router as game_router
from app.api.localdex.v1.localdex import router as localdex_router
from app.api.ops import router as ops_router
from app.api.status import router as status_router


app = FastAPI(lifespan=lifespan)


app.middleware("http")(maintenance_middleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(game_router, prefix="/api/guessamon/v1")
app.include_router(localdex_router, prefix="/api/localdex/v1")
app.include_router(ops_router, prefix="/ops")
app.include_router(status_router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")