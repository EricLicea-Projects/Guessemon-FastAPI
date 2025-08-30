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


def to_pokemon_data(raw_data: dict) -> PokemonData:
    types = [t['type']['name'] for t in raw_data.get('types', [])]
    abilities = [a['ability']['name'] for a in raw_data.get('abilities', [])]
    stats = [s['base_stat'] for s in raw_data.get('stats', [])]

    pokemon_id = raw_data.get('id')
    pokemon_name = raw_data.get('name', '')

    
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
        'height': raw_data.get('height'),
        'weight': raw_data.get('weight'),
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
