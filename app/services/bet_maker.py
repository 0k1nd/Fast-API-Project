from app.models import Event, Bet
from datetime import datetime
from sqlalchemy.orm import Session
from app.dto import bet
from app.dto.bet import EventStatusEnum
from fastapi import HTTPException

def get_events(db: Session):
    return db.query(Event).filter(Event.date_end_of_bets >= datetime.now()).all()

def create_bet(data: bet.Bet, db: Session):
    bet = Bet(
        event_id=data.event_id,
        amount=data.amount,
        is_win=data.is_win
    )
    try:
        db.add(bet)
        db.commit()
        db.refresh(bet)
        return bet
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_bets(db: Session):
    return db.query(Bet).all()

def update_stat(data: bet.BetWebhooks, db: Session):
    bets = db.query(Bet).filter(Bet.event_id == data.event_id).all()

    if not bets:
        return {"message": f"No bets found for event {data.event_id}"}

    is_win = data.event_stat == EventStatusEnum.win  # True/False

    for bet in bets:
        bet.is_win = is_win

    db.commit()  # Один `commit` на все изменения

    return {"message": f"Updated {len(bets)} bets for event {data.event_id}"}
