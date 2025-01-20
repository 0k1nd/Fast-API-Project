from bet_maker.models import Bet
from sqlalchemy.orm import Session
from bet_maker.dto import bet
from bet_maker.dto.bet import EventStatusEnum
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import requests
import httpx

async def create_bet(data: bet.Bet, db: AsyncSession):
    if not data:
        raise HTTPException(status_code=400, detail="Invalid request body")

    new_bet = Bet(
        event_id=data.event_id,
        amount=data.amount,
        is_win=data.is_win
    )

    try:
        db.add(new_bet)
        await db.commit()
        await db.refresh(new_bet)
        return new_bet
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_bets(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Bet))
        bets = result.scalars().all()
    return bets

async def update_stat(data: bet.BetWebhooks, db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Bet).filter(Bet.event_id == data.event_id).all())
        bets = result.scalars().all()

        if not bets:
            return {"message": f"No bets found for event {data.event_id}"}

        is_win = data.event_stat == EventStatusEnum.win

        for bet in bets:
            bet.is_win = is_win

        await db.commit()

    return {"message": f"Updated {len(bets)} bets for event {data.event_id}"}

async def send_request(url):
    async with httpx.AsyncClient() as client: 
        response = await client.get(url)
        return response.json()
