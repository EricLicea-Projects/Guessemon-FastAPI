from typing import Dict, Any, Literal
from app.schemas import PokemonData

Differences = Literal['higher', 'lower', 'equal']

def compare_numeric(guess_val: int | None, correct_val: int | None) -> Differences | None:
    """Return 'higher' | 'lower' | 'equal' comparing guess vs correct; None if missing."""

    if guess_val is None or correct_val is None:
        return None
    difference = guess_val - correct_val
    return 'higher' if difference > 0 else 'lower' if difference < 0 else 'equal'
    

def compare_pokemon_data(guess: PokemonData, correct: PokemonData) -> Dict[str, Any]:
    """Builds hints comparing a guessed Pokémon to the correct one."""

    guess_types = set(guess.types or [])
    correct_types = set(correct.types or [])

    types_comparison = {
        "shared": sorted(guess_types & correct_types),
        "guess": sorted(guess_types),
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
