from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# class StatusEnum(str, Enum):
#     win = "1win"
#     lose = "2win"

class Event(BaseModel):
    cof: float
    date_end_of_bets: datetime
    status: str = "pending"
    
    class Config:
        from_attributes = True