import uvicorn
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from app.config import DATABASE_URL, SECRET_KEY
from app.models import Admin
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI()
engine = create_async_engine(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await admin_app.init(
        admin_secret=SECRET_KEY,
        engine=engine,
        provider=UsernamePasswordProvider(
            admin_model=Admin,
            login_logo_url="https://fastapi-admin.github.io/img/logo.png"
        )
    )
    app.mount("/admin", admin_app)
