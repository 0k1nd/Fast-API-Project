import uvicorn
from fastapi import FastAPI
from app.database import Sessionlocal, engine, Base
from app.routers import bet_maker as BetRouter
from app.routers import line_provider as LineRouter

Base.metadata.create_all(bind=engine)

app= FastAPI()
app.include_router(BetRouter.router, prefix="/bet")
app.include_router(LineRouter.router, prefix="/event")
if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0',port=8000,reload=True,workers=3)
    print("---")