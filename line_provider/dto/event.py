from pydantic import  BaseModel
from datetime import datetime

class Event(BaseModel):
    cof: float
    date_end_of_bets: datetime
    status: str