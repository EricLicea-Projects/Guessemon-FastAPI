import random
from datetime import datetime

def get_pokemon_of_the_day() -> int:
    seed_value = int(datetime.now().strftime('%Y%j'))
    random.seed(seed_value)
    return  random.randint(1, 151)
    