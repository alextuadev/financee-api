
from fastapi import APIRouter
from config.database import Session
from services.transaction import TransactionService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

transaction_router = APIRouter()

@transaction_router.get('/transactions', tags=['transactions'])
def get_transactions():
    db = Session()
    result = TransactionService(db).get_transactions()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

