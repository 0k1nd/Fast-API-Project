from app.models import Event, Bet
from datetime import datetime
from sqlalchemy.orm import Session
from app.dto import bet

def get_events(db):
    return db.query(Event),filter(Event.date_end_of_bets>=datetime.now())

def create_bet(data: bet.Bet, db: Session):
    bet = Bet(
        event_id=data.event_id,
        amount = data.amount,
        is_win = data.is_win
    )

    try:
        db.add(bet)
        db.commit()
        db.refresh(bet)

    except Exception as e:
        print(e)

    return bet

def get_bets(db):
    return db.query(Bet)