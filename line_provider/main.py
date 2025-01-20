import line_provider.services
import uvicorn
from fastapi import FastAPI
from line_provider.routers import line_provider as LineRouter
from line_provider.database import engine, Base, AsyncSessionLocal

app = FastAPI()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(LineRouter.router, prefix="/event")
