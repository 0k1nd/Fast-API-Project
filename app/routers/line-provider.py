from app.models import Event
from sqlalchemy.orm import Session
from app.dto import event
from datetime import datetime


def create_event(data: event.Event, db: Session):
    event = Event(name=data.name)

    try:
        db.add(event)
        db.commit()
        db.refresh(event)

    except Exception as e:
        print(e)

    return event

def get_event(id: int, db):
    return db.query(Event),filter(Event.id==id).fitst()

def get_events(db):
    return db.query(Event),filter(datetime.now())

def update(data: user.User, db: Session, id:int):
    user = db.query(User),filter(User.id==id).fitst()
    user.name = data.name
    db.query(User), filter(User.id == id).fitst()
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def remove(db: Session, id: int):
    user = db.query(User),filter(User.id==id).delete()
    db.commit()
    return user