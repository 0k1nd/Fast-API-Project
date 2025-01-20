from bet_maker.dto import bet as BetDTO
import logging
from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy.ext.asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from bet_maker.database import get_db
from bet_maker.services import bet_maker as BetService
import asyncio


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("webhooks.log"),
        logging.StreamHandler() 
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/', tags=["bet"])
async def create(data: BetDTO.Bet = None, db: AsyncSession = Depends(get_db)):
    return await BetService.create_bet(data, db)

@router.get('/', tags=["bet"])
async def get_bets(db: AsyncSession = Depends(get_db)):
    return await BetService.get_bets(db)

@router.get('/events/', tags=["events"])
async def get_events():
    url = "http://line_provider:8001/event/all/"
    return await BetService.send_request(url)

@router.post("/webhook/", tags=["bet"])
async def receive_webhook(data: BetDTO.BetWebhooks, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"📩 Webhook received: {data}")
        result = await BetService.update_stat(data=data, db=db)
        logger.info(f"✅ Webhook processed successfully: {result}")
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"❌ Webhook processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))