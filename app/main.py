import os
from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader, APIKey

from app.schemas import GuessResponse
from pokemon_cache import get_cached_pokemon, clear_redis_cache
from app.services.hints import compare_pokemon_data


app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://guessemon.vercel.app",
    "https://guessamon.xyz",
    "https://www.guessamon.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API_KEY = os.getenv("API_KEY")
# if not API_KEY:
#     raise Exception("API_KEY environment variable is not set.")

# API_KEY_NAME = "access_token"
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# def get_api_key(api_key: str = Depends(api_key_header)):
#     if api_key == API_KEY:
#         return api_key
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#         )

# @app.get('/')
# async def read_root():
#     return {'message': 'Welcome to Guessamon API'}

# @app.post("/clear_cache")
# async def clear_cache_endpoint(api_key: APIKey = Depends(get_api_key)):
#     try:
#         await clear_redis_cache()
#         return {"message": "Redis cache cleared successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get('/pokemon_of_day')
async def pokemon_of_day():
    return await get_cached_pokemon()

@app.post('/guesses/{pokemon_id}', response_model = GuessResponse)
async def submit_guess(pokemon_id: int) -> GuessResponse:
    formatted_guess = await get_cached_pokemon(pokemon_id)
    formatted_correct = await get_cached_pokemon()
    hints = compare_pokemon_data(formatted_guess, formatted_correct)
    return GuessResponse(
        correct=(formatted_guess.id == formatted_correct.id),
        hints=hints
    )
