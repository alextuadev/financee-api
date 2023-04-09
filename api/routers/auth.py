from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from config.database import async_session
from schemas.user import User, UserLogin
from services.user import UserService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


auth_router = APIRouter()

@auth_router.post("/auth/login", tags=['auth'], response_model=dict, status_code=200)
async def login(userData: UserLogin):

    async with async_session() as db:
        response = await UserService(db).token(userData)
    
    return JSONResponse(status_code=200, content=response)


@auth_router.post('/auth/register', tags=['auth'], response_model=dict, status_code=201)
async def registration(user: User)->dict:
    async with async_session() as db:
        response = await UserService(db).register(user)

    return JSONResponse(status_code=201, content={"message": "Register Successfully", "data": response})