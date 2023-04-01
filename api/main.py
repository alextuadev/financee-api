from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.transaction import transaction_router
from routers.auth import auth_router

app = FastAPI()
app.version = "0.0.3"
app.title = "Finance API"
app.add_middleware(ErrorHandler)
app.include_router(auth_router)
app.include_router(transaction_router)


Base.metadata.create_all(bind=engine)

@app.get('/')
def message():
    return "Hello Financee API"

