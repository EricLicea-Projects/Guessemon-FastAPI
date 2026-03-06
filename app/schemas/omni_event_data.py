from typing import List, Annotated
from pydantic import BaseModel, Field
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
    url: str

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
    stalemates: int
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

class OmniCrudPayload(BaseModel):
    event: OmniEvent
    players: Annotated[list[OmniPlayer], Field(min_length=1)]
    standings: Annotated[list[OmniEventStanding], Field(min_length=1)]
    participants: Annotated[list[OmniEventParticipant], Field(min_length=1)]