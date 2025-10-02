from typing import List, Optional
from pydantic import BaseModel

class PokemonData(BaseModel):
    id: int
    name: str
    types: List[str]
    abilities: List[str]
    stats: List[int]
    height: Optional[float]
    weight: Optional[float]
    base_experience: Optional[int]
    capture_rate: Optional[int]
    color: Optional[str]
    flavor_text: Optional[str]
    generation: Optional[str]
    is_baby: Optional[bool]
    is_legendary: Optional[bool]
    is_mythical: Optional[bool]
    shape: Optional[str]