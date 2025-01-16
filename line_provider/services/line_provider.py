import requests
from line_provider.models import Event
from sqlalchemy.orm import Session
from line_provider.dto import event as EventDTO
from datetime import datetime

BET_MAKER_WEBHOOK_URL = "http://localhost:8000/bet/webhook/"

def create_event(data: EventDTO.Event, db: Session):
    event = Event(
        name=data.name,
        date_end_of_bets=data.date_end_of_bets,
        status=data.status
    )
    try:
        db.add(event)
        db.commit()
        db.refresh(event)

    except Exception as e:
        db.rollback()
        raise e
    return event

def get_event(id: int, db: Session):
    return db.query(Event).filter(Event.id == id).first()

def get_events(db: Session):
    return db.query(Event).filter(Event.date_end_of_bets >= datetime.now()).all()

def send_webhook(event_id: int, event_stat: str):
    payload = {
        "event_id": event_id,
        "event_stat": event_stat
    }

    try:
        response = requests.post(BET_MAKER_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        print(f"Webhook sent successfully: {payload}")
    except requests.RequestException as e:
        print(f"Error sending webhook: {e}")

def update(data: EventDTO.Event, db: Session, id: int):
    event = db.query(Event).filter(Event.id == id).first()
    if event:
        event.name = data.name
        event.date_end_of_bets = data.date_end_of_bets
        event.status = data.status
        event.cof = data.cof
        db.commit()
        db.refresh(event)

        if event.status == "1win" or "2win":
            send_webhook(event.id, event.status)

        return event
    else:
        raise ValueError(f"Event with ID {id} not found")


def remove(db: Session, id: int):
    event = db.query(Event).filter(Event.id == id).first()
    if event:
        db.delete(event)
        db.commit()
        return {"message": "Event deleted successfully"}
    else:
        raise ValueError(f"Event with ID {id} not found")
