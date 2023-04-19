from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.transaction import transaction_router
from routers.bank import bank_router
from routers.auth import auth_router
from routers.bank_account import bank_account_router
from routers.credit_card import credit_card_router
from routers.debt import debt_router
from routers.debt_type import debt_type_router


app = FastAPI()
app.version = "0.0.6"
app.title = "Financee API"
app.add_middleware(ErrorHandler)
app.include_router(auth_router, prefix="/api")
app.include_router(bank_router, prefix="/api")
app.include_router(bank_account_router, prefix="/api")
app.include_router(credit_card_router, prefix="/api")
app.include_router(debt_type_router, prefix="/api")
app.include_router(debt_router, prefix="/api")
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

