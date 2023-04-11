from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import  List
from models.transaction import Transaction as TransactionModel
from services.bank import BankService
from schemas.bank import Bank
from fastapi.security import HTTPBearer
from middlewares.jwt_auth import JWTBearer
from config.database import async_session

bank_router = APIRouter()


@bank_router.get('/banks', tags=['banks'], dependencies=[Depends(JWTBearer())])
async def get_banks():
    async with async_session() as db:
        banks = await BankService(db).get_banks()

    response = jsonable_encoder(banks)
    return JSONResponse(status_code=200, content=response)


@bank_router.get('/banks/{id}', tags=['banks'], dependencies=[Depends(JWTBearer())])
async def get_bank(id: int = Path(ge=1, le=2000)) -> Bank:
    async with async_session() as db:
        result = await BankService(db).get_bank(id)

    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@bank_router.post('/banks', tags=['banks'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
async def create_bank(bank: Bank) -> dict:
    async with async_session() as db:
        await BankService(db).create_bank(bank)

    return JSONResponse(status_code=201, content={"message": "Bank created"})


@bank_router.put('/banks/{id}', tags=['banks'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
async def update_bank(id: int, bank: Bank) -> dict:
    async with async_session() as db:
        updated_bank = await BankService(db).update_bank(id, bank)

    if not updated_bank:
        return JSONResponse(status_code=404, content={"message": "Bank not found"})
    
    return JSONResponse(status_code=200, content={"message": "Bank updated", "bank": jsonable_encoder(updated_bank)})


@bank_router.delete('/banks/{id}', tags=['banks'], response_model=dict, status_code=200,  dependencies=[Depends(JWTBearer())])
async def delete_bank(id: int) -> dict:
    async with async_session() as db:
        deleted = await BankService(db).delete_bank(id)

    if not deleted:
        return JSONResponse(status_code=404, content={"message": "Bank not found"})
    
    return JSONResponse(status_code=200, content={"message": "Bank deleted"})