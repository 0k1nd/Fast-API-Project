from bet_maker.dto import bet as BetDTO
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bet_maker.database import get_db
from bet_maker.services import bet_maker as BetService
import asyncio


logging.basicConfig(
    level=logging.INFO,  # Можно сменить на DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("webhooks.log"),  # Логи в файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/', tags=["bet"])
async def create(data: BetDTO.Bet = None, db: Session = Depends(get_db)):
    return BetService.create_bet(data, db)

@router.get('/', tags=["bet"])
async def get_bets(db: Session = Depends(get_db)):
    return BetService.get_bets(db)

@router.get('/events/', tags=["events"])
async def get_events():
    url = "http://line_provider:8001/event/all/"
    return BetService.send_request(url)

@router.post("/webhook/", tags=["bet"])
async def receive_webhook(data: BetDTO.BetWebhooks, db: Session = Depends(get_db)):
    try:
        logger.info(f"📩 Webhook received: {data}")
        result = BetService.update_stat(data=data, db=db)
        logger.info(f"✅ Webhook processed successfully: {result}")
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"❌ Webhook processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))