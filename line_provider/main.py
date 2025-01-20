import uvicorn
from fastapi import FastAPI
from line_provider.database import engine, Base
from line_provider.routers import line_provider as LineRouter

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(LineRouter.router, prefix="/event")
