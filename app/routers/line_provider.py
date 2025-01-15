from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.services import line_provider as EventService
from app.dto import event as EventDTO

router = APIRouter()

@router.post('/', tags=["event"])
async def create(data: EventDTO.Event = None, db: Session = Depends(get_db)):
    return EventService.create_event(data, db)

@router.get('/{id}', tags=["event"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return EventService.get_event(db,id)

@router.put('/{id}', tags=["event"])
async def update(id: int = None,data:EventDTO.Event = None, db: Session = Depends(get_db)):
    return EventService.update(data,db,id)

@router.delete('/{id}', tags=["event"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return EventService.remove(db,id)