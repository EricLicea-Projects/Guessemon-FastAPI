from typing import List
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class OmniEventData(BaseModel):
    event: dict
    players: List
    standings: dict
    rounds: List

class OmniEvent(BaseModel):
    event_id: int
    ranked: bool
    players: List
    judges: List
    swiss_match_config: str
    swiss_rounds: int
    start_at: datetime
    url: HttpUrl

class OmniPlayer(BaseModel):
    player_id: int
    username: str
    country: str
    player_cp: int
    player_rank: int
    player_emblem: str

class OmniEventStanding(BaseModel):
    event_id: int
    player_id: int
    placement: int
    wins: int
    losses: int
    ties: int
    byes: int
    score: int

class OmniEventParticipant(BaseModel):
    event_id: int
    player_id: int
    round_id: int
    pairing_id: int
    dropped: bool
    score: int
    status: str
    elo_change: float