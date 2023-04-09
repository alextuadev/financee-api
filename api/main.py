from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.transaction import transaction_router
from routers.auth import auth_router


app = FastAPI()
app.version = "0.0.4"
app.title = "Financee API"
app.add_middleware(ErrorHandler)
app.include_router(auth_router, prefix="/api")
# app.include_router(transaction_router, prefix="/api")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get('/')
def message():
    return "Hello Financee API"

