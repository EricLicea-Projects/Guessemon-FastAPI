from pydantic import BaseModel
from typing import List, Optional

class PokemonData(BaseModel):
    id: int
    name: str
    types: List[str]
    abilities: List[str]
    stats: List[int]
    height: Optional[int]
    weight: Optional[int]
    base_experience: Optional[int]

def format_pokemon_data(raw_data: dict) -> PokemonData:

    types = [t['type']['name'] for t in raw_data.get('types', [])]
    abilities = [a['ability']['name'] for a in raw_data.get('abilities', [])]
    stats = [s['base_stat'] for s in raw_data.get('stats', [])]

    data = {
        'id': raw_data.get('id'),
        'name': raw_data.get('name'),
        'types': types,
        'abilities': abilities,
        'stats': stats,
        'height': raw_data.get('height'),
        'weight': raw_data.get('weight'),
        'base_experience': raw_data.get('base_experience'),
    }

    return PokemonData(**data)