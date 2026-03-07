from typing import List, Annotated
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