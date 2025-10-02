import random, re
from app.schemas import PokemonData


def _pick_english_flavor_text(entries: list[dict], pokemon_name: str, pokemon_id: int)-> str:
    english = [
        entry.get('flavor_text', '')
        .replace('\n', ' ')
        .replace('\u000c', ' ')
        .strip()
        for entry in entries
        if entry.get('language', {}).get('name') == 'en'
    ]

    if not english:
        return ''
    
    text = random.Random(pokemon_id).choice(english)
    return re.sub(re.escape(pokemon_name), '*' * len(pokemon_name), text, flags=re.IGNORECASE) if pokemon_name else text

def _to_meters(height_dm):
    return height_dm / 10 if isinstance(height_dm, (int, float)) else None

def _to_kilograms(weight_hg):
    return weight_hg / 10 if isinstance(weight_hg, (int, float)) else None

def to_pokemon_data(raw_data: dict) -> PokemonData:
    types = [t['type']['name'] for t in raw_data.get('types', [])]
    abilities = [a['ability']['name'] for a in raw_data.get('abilities', [])]
    stats = [s['base_stat'] for s in raw_data.get('stats', [])]

    pokemon_id = raw_data.get('id')
    pokemon_name = raw_data.get('name', '')

    height_m = _to_meters(raw_data.get('height'))
    weight_kg = _to_kilograms(raw_data.get('weight'))

    
    flavor_text = _pick_english_flavor_text(
        raw_data.get('flavor_text_entries', []),
        pokemon_name,
        pokemon_id,
    )

    data = {
        'id': pokemon_id,
        'name': pokemon_name,
        'types': types,
        'abilities': abilities,
        'stats': stats,
        'height': height_m,
        'weight': weight_kg,
        'base_experience': raw_data.get('base_experience'),
        'capture_rate': raw_data.get('capture_rate'),
        'color': raw_data.get('color', {}).get('name'),
        'flavor_text': flavor_text,
        'generation': raw_data.get('generation', {}).get('name'),
        'is_baby': raw_data.get('is_baby'),
        'is_legendary': raw_data.get('is_legendary'),
        'is_mythical': raw_data.get('is_mythical'),
        'shape': raw_data.get('shape', {}).get('name'),
    }

    return PokemonData(**data)
