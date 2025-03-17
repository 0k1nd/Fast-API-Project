from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from line_provider.app.db.database import get_db
from line_provider.services import line_provider as EventService
from line_provider.dto import event as EventDTO
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post('/', tags=["event"])
async def create(data: EventDTO.Event, db: AsyncSession = Depends(get_db)):
    try:
        return await EventService.create_event(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/all/', tags=["event"])
async def get_events(db: AsyncSession = Depends(get_db)):
    return await EventService.get_events(db)

@router.get('/{id}', tags=["event"])
async def get(id: int, db: AsyncSession = Depends(get_db)):
    event = await EventService.get_event(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put('/{id}', tags=["event"])
async def update(id: int, data: EventDTO.Event, db: AsyncSession = Depends(get_db)):
    try:
        return await EventService.update(data, db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{id}', tags=["event"])
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await EventService.remove(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
