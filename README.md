# Guessamon API (FastAPI)

A backend for the Guessamon game built with [FastAPI](https://fastapi.tiangolo.com/). It fetches Pokémon data from [PokeAPI](https://pokeapi.co/), maps it into game-friendly “hints” that the frontend uses during guessing, and caches both the formatted Pokémon data and hints in [Redis](https://redis.io/) to avoid repeated upstream calls during multiple guesses.

