from fastapi import APIRouter
from fastapi import Depends, HTTPException, Path, Query, Request
# from config.database import Session
from services.transaction import TransactionService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import  List
from models.transaction import Transaction as TransactionModel
from services.transaction import TransactionService
from schemas.transaction import Transaction
from fastapi.security import HTTPBearer
from middlewares.jwt_auth import JWTBearer


transaction_router = APIRouter()


@transaction_router.get('/transactions', tags=['transactions'], dependencies=[Depends(JWTBearer())])
def get_transactions():
    db = Session()
    result = TransactionService(db).get_transactions()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@transaction_router.get('/transactions/{id}', tags=['transactions'])
def get_transaction(id: int = Path(ge=1, le=2000)) -> Transaction:
    db = Session()
    result = TransactionService(db).get_transactions()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@transaction_router.post('/transactions', tags=['transactions'], response_model=dict, status_code=201)
def create_transaction(transaction: Transaction) -> dict:
    db = Session()
    TransactionService(db).create_transaction(transaction)
    return JSONResponse(status_code=201, content={"message": "Transaction created"})


@transaction_router.get('/movies/', tags=['movies'], response_model=List[Transaction])
def get_movies_by_category(category_id: int = Query()) -> List[Transaction]:
    db = Session()
    result = TransactionService(db).get_transaction_by_category(category_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@transaction_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_transaction(id: int, transaction: Transaction)-> dict:
    db = Session()
    result = TransactionService(db).get_transaction(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    TransactionService(db).update_transaction(id, transaction)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})


@transaction_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_transaction(id: int)-> dict:
    db = Session()
    result = db.query(TransactionModel).filter(TransactionModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "The transaction has been deleted"})