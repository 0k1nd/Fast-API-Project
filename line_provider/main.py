import uvicorn
from fastapi import FastAPI
from line_provider.database import engine, Base
from line_provider.routers import line_provider as LineRouter

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(LineRouter.router, prefix="/event")
if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0',port=8001,reload=True,workers=2)
    print("---")