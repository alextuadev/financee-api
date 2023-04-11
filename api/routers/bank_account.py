from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Path
from fastapi.responses import JSONResponse
from services.bank_account import BankAccountService
from schemas.bank_account import BankAccount
from middlewares.jwt_auth import JWTBearer
from config.database import async_session


bank_account_router = APIRouter()


@bank_account_router.get('/bank_accounts', tags=['bank_accounts'], dependencies=[Depends(JWTBearer())])
async def get_banks():
    async with async_session() as db:
        bank_accounts = await BankAccountService(db).get_bank_accounts()

    response = jsonable_encoder(bank_accounts)
    return JSONResponse(status_code=200, content=response)


@bank_account_router.get('/bank_accounts/{id}', tags=['bank_accounts'], dependencies=[Depends(JWTBearer())])
async def get_bank(id: int = Path(ge=1, le=2000)) -> BankAccount:
    async with async_session() as db:
        result = await BankAccountService(db).get_bank_account(id)

    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@bank_account_router.post('/bank_accounts', tags=['bank_accounts'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
async def create_bank(bankAccount: BankAccount) -> dict:
    async with async_session() as db:
        await BankAccountService(db).create_bank_account(bankAccount)

    return JSONResponse(status_code=201, content={"message": "Bank account created"})


@bank_account_router.put('/bank_accounts/{id}', tags=['bank_accounts'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
async def update_bank(id: int, bankAccount: BankAccount) -> dict:
    async with async_session() as db:
        updated_bank = await BankAccountService(db).update_bank_account(id, bankAccount)

    if not updated_bank:
        return JSONResponse(status_code=404, content={"message": "Bank not found"})
    
    return JSONResponse(status_code=200, content={"message": "Bank updated", "bank": jsonable_encoder(updated_bank)})


@bank_account_router.delete('/bank_accounts/{id}', tags=['bank_accounts'], response_model=dict, status_code=200,  dependencies=[Depends(JWTBearer())])
async def delete_bank(id: int) -> dict:
    async with async_session() as db:
        deleted = await BankAccountService(db).delete_bank_account(id)

    if not deleted:
        return JSONResponse(status_code=404, content={"message": "Bank not found"})
    
    return JSONResponse(status_code=200, content={"message": "Bank deleted"})