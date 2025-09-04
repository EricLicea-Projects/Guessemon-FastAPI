# Guessamon API (FastAPI)

A backend for the Guessamon game built with [FastAPI](https://fastapi.tiangolo.com/). It fetches Pokémon data from [PokeAPI](https://pokeapi.co/), maps it into game-friendly “hints” that the frontend uses during guessing, and caches both the formatted Pokémon data and hints in [Redis](https://redis.io/) to avoid repeated upstream calls during multiple guesses.

## Quickstart

**Prereqs**
- Python 3.11+
- A Redis instance (local or hosted). Default local URL: `redis://127.0.0.1:6379`

**Run**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
