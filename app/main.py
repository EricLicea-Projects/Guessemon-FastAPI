from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.settings import settings
from app.core.lifespan import lifespan
from app.api.v1.game import router as game_router
from app.api.ops import router as ops_router


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
