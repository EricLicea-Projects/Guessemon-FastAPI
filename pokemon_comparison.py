from typing import Dict, Any
from pokemon_parser import PokemonData

def compare_numeric(guess_val: int | None, correct_val: int | None) -> str | None:
    if guess_val is None or correct_val is None:
        return None
    if guess_val > correct_val:
        return "higher"
    elif guess_val < correct_val:
        return "lower"
    else:
        return "equal"
    

def compare_pokemon_data(guess: PokemonData, correct: PokemonData) -> Dict[str, Any]:

    guess_types = set(guess.types or [])
    correct_types = set(correct.types or [])
    types_comparison = {
        "common": list(guess_types.intersection(correct_types)),
        "guess_only": list(guess_types - correct_types),
        "correct_only": list(correct_types - guess_types)
    }
    
    comparison_result = {
        "types": types_comparison,
        "color": guess.color == correct.color,
        "habitat": guess.habitat == correct.habitat,
        "shape": guess.shape == correct.shape,
        "height": compare_numeric(guess.height, correct.height),
        "weight": compare_numeric(guess.weight, correct.weight)
    }
    
    return comparison_result    
