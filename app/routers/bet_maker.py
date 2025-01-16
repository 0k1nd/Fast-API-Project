from app.dto import bet as BetDTO
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import bet_maker as BetService


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

@router.get('/events/', tags=["bet"])
async def get_events(db: Session = Depends(get_db)):
    return BetService.get_events(db)


@router.post("/webhook/", tags=["bet"])
async def receive_webhook(data: BetDTO.BetWebhooks, db: Session = Depends(get_db)):
    """
    Принимает вебхук от `line-provider` и обновляет ставки (`bet-maker`).
    """
    try:
        logger.info(f"📩 Webhook received: {data}")  # Логируем входящий запрос
        result = BetService.update_stat(data=data, db=db)
        logger.info(f"✅ Webhook processed successfully: {result}")  # Логируем успех
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"❌ Webhook processing error: {str(e)}")  # Логируем ошибку
        raise HTTPException(status_code=400, detail=str(e))