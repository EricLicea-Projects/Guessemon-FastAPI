from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime

class LocalEvent(BaseModel):
    event_id: int
    ranked: bool
    swiss_match_config: str
    swiss_rounds: int
    start_at: datetime
    url: str

class LocalStanding(BaseModel):
    placement: int
    username: str
    player_id: int
    wins: int
    losses: int
    stalemates: int
    byes: int
    score: int
    main_element_id: int
    champion_id: int
    main_element: str
    champion_element: str
    champion_name: str
    champion_class: str
    champion_sub_class: Optional[str] = None

class MainElementPlayRate(BaseModel):
    element_name: str
    times_played: int
    play_rate: float

class TopChampion(BaseModel):
    champion_id: int
    champion_name: str
    times_played: int

class PlayerStats(BaseModel):
    player_id: int
    username: str
    player_cp: int
    games_played: int
    win_rate: Decimal
    main_element_id: int
    main_element: str
    top_3_champions: list[TopChampion]

class Element(BaseModel):
    element_id: int
    element_name: str


class ChampionStats(BaseModel):
    champion_id: int
    champion_name: str
    pick_rate: float
    win_rate: float
    top_elements: list[Element]
