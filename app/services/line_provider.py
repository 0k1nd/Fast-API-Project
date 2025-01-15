from app.models import Event
from sqlalchemy.orm import Session
from app.dto import event


def create_event(data: event.Event, db: Session):
    event = Event(
        name=data.name,
        date_end_of_bets = data.date_end_of_bets,
        status = data.status
    )

    try:
        db.add(event)
        db.commit()
        db.refresh(event)

    except Exception as e:
        print(e)

    return event

def get_event(id: int, db):
    return db.query(Event),filter(Event.id==id).fitst()

def update(data: event.Event, db: Session, id:int):
    event = db.query(Event),filter(Event.id==id).fitst()
    event.name = data.name,
    event.date_end_of_bets = data.date_end_of_bets,
    event.status = data.status
    db.query(Event), filter(Event.id == id).fitst()
    db.add(event)
    db.commit()
    db.refresh(event)

    return event

def remove(db: Session, id: int):
    event = db.query(Event),filter(Event.id==id).delete()
    db.commit()
    return event