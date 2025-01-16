from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import line_provider as EventService
from app.dto import event as EventDTO

router = APIRouter()

@router.post('/', tags=["event"])
async def create(data: EventDTO.Event, db: Session = Depends(get_db)):
    try:
        return EventService.create_event(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/{id}', tags=["event"])
async def get(id: int, db: Session = Depends(get_db)):
    event = EventService.get_event(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put('/{id}', tags=["event"])
async def update(id: int, data: EventDTO.Event, db: Session = Depends(get_db)):
    try:
        return EventService.update(data, db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{id}', tags=["event"])
async def delete(id: int, db: Session = Depends(get_db)):
    try:
        return EventService.remove(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
