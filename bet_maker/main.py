from bet_maker.routers import bet_maker as BetRouter
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from bet_maker.database import engine, Base, AsyncSessionLocal

app = FastAPI()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(BetRouter.router, prefix="/bet")
