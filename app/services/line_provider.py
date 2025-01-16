from app.models import Event
from sqlalchemy.orm import Session
from app.dto import event as EventDTO

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

def update(data: EventDTO.Event, db: Session, id: int):
    event = db.query(Event).filter(Event.id == id).first()
    if event:
        event.name = data.name
        event.date_end_of_bets = data.date_end_of_bets
        event.status = data.status
        db.commit()
        db.refresh(event)
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
