from typing import Dict, Any
from app.schemas import PokemonData

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
        "shared": list(guess_types.intersection(correct_types)),
        "guess": list(guess_types),
        "guess_single": len(guess_types) == 1,
        "correct_single": len(correct_types) == 1,
        "both_single": (len(guess_types) == 1 and len(correct_types) == 1)
    }
    
    comparison_result = {
        "id": guess.id,
        "types": types_comparison,
        "color": {
            "is_correct": guess.color == correct.color,
            "guess": guess.color,
        },
        "generation": {
            "is_correct": guess.generation == correct.generation,
            "guess": guess.generation,
        },
        "shape": {
            "is_correct": guess.shape == correct.shape,
            "guess": guess.shape,
        },
        "height": compare_numeric(guess.height, correct.height),
        "weight": compare_numeric(guess.weight, correct.weight)
    }
    
    return comparison_result    
