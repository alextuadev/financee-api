from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from config.database import engine, Base
from models.category import Category
from models.user import User
from models.transaction import Transaction
from pydantic import BaseModel, Field
from middlewares.jwt_auth import JWTBearer
from middlewares.error_handler import ErrorHandler
from routers.transaction import transaction_router


app = FastAPI()
app.version = "0.0.2"
app.title = "Finance API"
app.add_middleware(ErrorHandler)
app.include_router(transaction_router)


Base.metadata.create_all(bind=engine)


@app.get('/')
def message():
    return "Hello Financee API"

