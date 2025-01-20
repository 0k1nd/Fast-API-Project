import uvicorn
from fastapi import FastAPI
from bet_maker.database import Sessionlocal, engine, Base
from bet_maker.routers import bet_maker as BetRouter

Base.metadata.create_all(bind=engine)

app= FastAPI()
app.include_router(BetRouter.router, prefix="/bet")
