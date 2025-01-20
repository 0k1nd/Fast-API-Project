import requests
import httpx
import asyncio
from sqlalchemy.orm import selectinload
from line_provider.models import Event
from sqlalchemy.ext.asyncio import AsyncSession
from line_provider.dto import event as EventDTO
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException

BET_MAKER_WEBHOOK_URL = "http://bet_maker:8000/bet/webhook/"

async def create_event(data: EventDTO.Event, db: AsyncSession):
    if not data:
        raise HTTPException(status_code=400, detail="Received None instead of event data")
    
    event = Event(
        date_end_of_bets=data.date_end_of_bets.replace(tzinfo=None),
        status= data.status,
        cof = data.cof
    )
    try:
        db.add(event)
        await db.commit()
        await db.refresh(event)

    except Exception as e:
        await db.rollback()
        raise e
    return event

async def get_event(id: int, db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Event).filter(Event.id == id))
        event = result.scalars().first()
    return event

async def get_events(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Event).filter(Event.date_end_of_bets >= datetime.now()))
        events = result.scalars().all()
    return events

async def send_webhook(event_id: int, event_stat: str):
    payload = {
        "event_id": event_id,
        "event_stat": event_stat
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BET_MAKER_WEBHOOK_URL, json=payload, timeout=5)
            response.raise_for_status()
            print(f"Webhook sent successfully: {payload}")
        except httpx.RequestError as e:
            print(f"Error sending webhook: {e}")

async def update(data: EventDTO.Event, db: AsyncSession, id: int):
    result = await db.execute(select(Event).filter(Event.id == id))
    event = result.scalars().first()
    if event:
        event.date_end_of_bets = data.date_end_of_bets
        event.status = data.status
        event.cof = data.cof
        await db.commit()
        await db.refresh(event)

        if event.status in ["1win", "2win"]:
            await send_webhook(event.id, event.status)

        return event
    else:
        raise ValueError(f"Event with ID {id} not found")


async def remove(db: AsyncSession, id: int):
    result = await db.execute(select(Event)).filter(Event.id == id)
    event = result.scalars().first()
    if event:
        await db.delete(event)
        await db.commit()
        return {"message": "Event deleted successfully"}
    else:
        raise ValueError(f"Event with ID {id} not found")
