from enum import Enum
from pydantic import  BaseModel
from typing import Optional

class Bet(BaseModel):
    event_id: int
    amount: float
    is_win: bool = False

    class Config:
        from_attributes = True

class EventStatusEnum(str, Enum):
    win = "1win"
    loss = "2win"

class BetWebhooks(BaseModel):
    event_id: int
    event_stat: EventStatusEnum