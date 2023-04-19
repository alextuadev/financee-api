# routers/debt_type_router.py
from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import JSONResponse
from config.database import async_session
from schemas.debt_type import DebtTypeCreate, DebtTypeUpdate, DebtType
from services.debt_type import DebtTypeService
from middlewares.jwt_auth import JWTBearer
from typing import List


debt_type_router = APIRouter()

@debt_type_router.post("/debt_types", response_model=DebtType, dependencies=[Depends(JWTBearer())])
async def create_debt_type(debt_type: DebtTypeCreate):
    async with async_session() as db:
        new_debt_type = await DebtTypeService(db).create_debt_type(debt_type)

    return JSONResponse(status_code=201, content=new_debt_type)

@debt_type_router.get("/debt_types", response_model=List[DebtType], dependencies=[Depends(JWTBearer())])
async def get_debt_types():
    async with async_session() as db:
        debt_types = await DebtTypeService(db).get_debt_types()
    return JSONResponse(status_code=200, content=debt_types)

@debt_type_router.get("/debt_types/{id}", response_model=DebtType, dependencies=[Depends(JWTBearer())])
async def get_debt_type(id: int = Path(ge=1)):
    async with async_session() as db:
        debt_type = await DebtTypeService(db).get_debt_type(id)
    return JSONResponse(status_code=200, content=debt_type)

@debt_type_router.put("/debt_types/{id}", response_model=DebtType, dependencies=[Depends(JWTBearer())])
async def update_debt_type(debt_type: DebtTypeUpdate, id: int = Path(ge=1)):
    async with async_session() as db:
        updated_debt_type = await DebtTypeService(db).update_debt_type(id, debt_type)

    return JSONResponse(status_code=200, content=updated_debt_type)

@debt_type_router.delete("/debt_types/{id}", response_model=DebtType, dependencies=[Depends(JWTBearer())])
async def delete_debt_type(id: int = Path(ge=1)):
    async with async_session() as db:
        deleted_debt_type = await DebtTypeService(db).delete_debt_type(id)
        if not deleted_debt_type:
            raise HTTPException(status_code=404, detail="Debt type not found")
    return JSONResponse(status_code=200, content={"message": "Debt type deleted"})
