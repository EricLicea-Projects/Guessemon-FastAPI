# Guessamon API (FastAPI)

A backend for the [Guessamon](https://www.guessamon.xyz/) game built with [FastAPI](https://fastapi.tiangolo.com/). It fetches Pokémon data from [PokeAPI](https://pokeapi.co/), maps it into game-friendly “hints” that the frontend uses during guessing, and caches both the formatted Pokémon data and hints in [Redis](https://redis.io/) to avoid repeated upstream calls during multiple guesses.

## Quickstart

**Prereqs**
- Python 3.11+
- A Redis instance (local or hosted). Default local URL: `redis://127.0.0.1:6379`

**Run**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

### GET `/api/v1/pokemon_of_day`
Returns the current (UTC-based) Pokémon, already mapped for the game.

```bash
curl http://127.0.0.1:8000/api/v1/pokemon_of_day
```
#### Pokemon Data
```json
{
  "id": 25,
  "name": "pikachu",
  "types": ["electric"],
  "abilities": ["static","lightning-rod"],
  "stats": [35,55,40,50,50,90],
  "height": 4,
  "weight": 60,
  "base_experience": 112,
  "capture_rate": 190,
  "color": "yellow",
  "flavor_text": "When several of these POKéMON gather...",
  "generation": "generation-i",
  "is_baby": false,
  "is_legendary": false,
  "is_mythical": false,
  "shape": "quadruped"
}
```
### Notes
- Cached in Redis and rolls over at the next UTC midnight.

### POST `/api/v1/guesses/{pokemon_id}`
Compares your guess to the correct Pokémon and returns whether it’s correct. If not correct, it will include a hints object to assist the player on their next guess.
```bash
curl -X POST http://127.0.0.1:8000/api/v1/guesses/25
```
#### Guess Response
```json
{
  "correct": false,
  "hints": {
    "id": 25,
    "types": {
      "shared": ["electric"],
      "guess": ["electric"],
      "guess_single": true,
      "correct_single": true,
      "both_single": true
    },
    "color": { "is_correct": false, "guess": "yellow" },
    "generation": { "is_correct": true, "guess": "generation-i" },
    "shape": { "is_correct": false, "guess": "quadruped" },
    "height": "higher",
    "weight": "lower"
  }
}
```
