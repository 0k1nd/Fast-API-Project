from app.models import Event, Bet
from datetime import datetime
from app.dto import bet

def get_events(db):
    return db.query(Event),filter(Event.date_end_of_bets>=datetime.now())