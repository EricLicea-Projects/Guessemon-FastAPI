import random
from datetime import date, datetime, timezone


MAX_POKEMON_ID = 1025

def pokemon_of_day(today: date | None = None) -> int:
    day = today or datetime.now(timezone.utc).date()
    seed_value = int(day.strftime('%Y%j'))
    rng = random.Random(seed_value)
    return rng.randint(1, MAX_POKEMON_ID)