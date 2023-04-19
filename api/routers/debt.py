from fastapi import APIRouter, Path, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_auth import JWTBearer
from fastapi.responses import JSONResponse
from config.database import async_session
from services.debt import DebtService
from schemas.debt import Debt
from typing import List

debt_router = APIRouter()

@debt_router.post("/debts", tags=["debts"], response_model=Debt, dependencies=[Depends(JWTBearer())])
async def create_debt(request: Request, debt: Debt):
    user_id = request.state.user_id
    async with async_session() as db:
        new_debt = await DebtService(db).create_debt(debt, user_id)
    return JSONResponse(status_code=201, content=jsonable_encoder(new_debt))


@debt_router.get("/debts", tags=["debts"], response_model=List[Debt], dependencies=[Depends(JWTBearer())])
async def get_debts(request: Request):
    user_id = request.state.user_id
    async with async_session() as db:
        debts = await DebtService(db).get_debts(user_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(debts))

@debt_router.get("/debts/{id}", tags=["debts"], response_model=Debt, dependencies=[Depends(JWTBearer())])
async def get_debt(request: Request, id: int = Path(ge=1, le=2000)):
    user_id = request.state.user_id
    async with async_session() as db:
        debt = await DebtService(db).get_debt(id, user_id)
        if not debt:
            raise HTTPException(status_code=404, detail="Debt not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(debt))

@debt_router.put("/debts/{id}", tags=["debts"], response_model=Debt, dependencies=[Depends(JWTBearer())])
async def update_debt(request: Request, debt: Debt, id: int = Path(ge=1, le=2000)):
    user_id = request.state.user_id
    async with async_session() as db:
        updated_debt = await DebtService(db).update_debt(id, debt, user_id)
        if not updated_debt:
            raise HTTPException(status_code=404, detail="Debt not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(updated_debt))

@debt_router.delete("/debts/{id}", tags=["debts"], dependencies=[Depends(JWTBearer())])
async def delete_debt(request: Request,id: int = Path(ge=1, le=2000)):
    user_id = request.state.user_id
    async with async_session() as db:
        deleted = await DebtService(db).delete_debt(id, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Debt not found")
    return JSONResponse(status_code=200, content={"message": "Debt deleted"})