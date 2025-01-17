from bet_maker.models import Bet
from sqlalchemy.orm import Session
from bet_maker.dto import bet
from bet_maker.dto.bet import EventStatusEnum
from fastapi import HTTPException
import requests

def create_bet(data: bet.Bet, db: Session):
    bet = Bet(
        event_id=data.event_id,
        amount=data.amount,
        is_win="false"
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

    is_win = data.event_stat == EventStatusEnum.win

    for bet in bets:
        bet.is_win = is_win

    db.commit()

    return {"message": f"Updated {len(bets)} bets for event {data.event_id}"}

def send_request(url):
    response = requests.get(url)
    return response.json()
