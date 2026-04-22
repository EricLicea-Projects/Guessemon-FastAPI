from typing import Optional
from pydantic import BaseModel, Field
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

class PlayerStats(BaseModel):
    player_id: int
    username: str
    player_cp: int
    total_wins: int
    total_losses: int
    total_games: int
    win_rate: float
    main_element: str
    top_3_champions: list[str] = Field(default_factory=list)
