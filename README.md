# Guessamon API (FastAPI)

Backend for the Guessamon game.  
Provides a *Pokémon of the day* (UTC-based) and compares user guesses against it. Caches results in Redis.

## Tech
- FastAPI
- Redis
- httpx
- Pydantic v2

## Endpoints

### GET `/api/v1/pokemon_of_day`
Returns the current Pokémon (formatted).

```bash
curl http://127.0.0.1:8000/api/v1/pokemon_of_day
