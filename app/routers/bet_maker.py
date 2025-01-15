from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.services import bet_maker as BetService
from app.dto import bet as BetDTO

router = APIRouter()

@router.post('/', tags=["bet"])
async def create(data: BetDTO.Bet = None, db: Session = Depends(get_db)):
    return BetService.create_bet(data, db)

@router.get('/{id}', tags=["bet"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return BetService.get_event(db,id)

@router.get('/', tags=["bet"])
async def get(db: Session = Depends(get_db)):
    return BetService.get_events(db)
