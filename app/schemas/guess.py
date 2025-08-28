from typing import Dict, Optional
from pydantic import BaseModel

class GuessResponse(BaseModel):
    correct: bool
    hints: Optional[Dict] = None