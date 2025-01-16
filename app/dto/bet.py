from pydantic import  BaseModel
from typing import Optional

class Bet(BaseModel):
    event_id: int
    amount: float
    is_win: Optional[bool]

    class Config:
        orm_mode = True