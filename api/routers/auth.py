from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from config.database import Session
from schemas.user import User, UserLogin
from services.user import UserService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


auth_router = APIRouter()

@auth_router.post("/auth/login", tags=['auth'], response_model=dict, status_code=200)
async def login(userData: UserLogin):
    db = Session()  
    response = UserService(db).token(userData)

    return JSONResponse(status_code=200, content=response)


@auth_router.post('/auth/register', tags=['auth'], response_model=dict, status_code=201)
def registration(user: User)->dict: 
    db = Session()  
    UserService(db).register(user)
    return JSONResponse(status_code=201, content={"message": "Register Successfully"})