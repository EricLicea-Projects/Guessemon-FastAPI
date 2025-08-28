import random
import re
from app.schemas import PokemonData


def format_pokemon_data(raw_data: dict) -> PokemonData:
    types = [t['type']['name'] for t in raw_data.get('types', [])]
    abilities = [a['ability']['name'] for a in raw_data.get('abilities', [])]
    stats = [s['base_stat'] for s in raw_data.get('stats', [])]

    flavor_text_entries = raw_data.get('flavor_text_entries', [])
    english_flavor_texts = [
        entry.get('flavor_text', '')
        .replace('\n', ' ')
        .replace('\u000c', ' ')
        .strip()
        for entry in flavor_text_entries
        if entry.get('language', {}).get('name') == 'en'
    ]

    flavor_text = random.choice(english_flavor_texts) if english_flavor_texts else None

    pokemon_name = raw_data.get('name', '')
    if flavor_text and pokemon_name:
        name_pattern = re.escape(pokemon_name)
        flavor_text = re.sub(name_pattern, '*' * len(pokemon_name), flavor_text, flags=re.IGNORECASE)

    data = {
        'id': raw_data.get('id'),
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
