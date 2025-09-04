# Guessamon API (FastAPI)

A FastAPI backend for my Guessamon game. It fetches Pokémon data from PokeAPI, formats it into a clean schema, caches results in Redis, and exposes simple endpoints for my frontend.

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
