from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder

from middlewares.jwt_auth import JWTBearer
from middlewares.error_handler import ErrorHandler


auth_router = APIRouter()


class User(BaseModel):
    name:str = Field(min_length=5, max_length=150)
    email:str = Field(min_length=5, max_length=150)
    password:str = Field(min_length=8, max_length=150)
    active:bool

    class Config:
        schema_extra = {
            "example": {
                "name": "Username",
                "email": "email@email.com",
                "password": "123456789",
                "active": True
            }
        }

#auth_router.post('/auth/login', tags=['auth'], response_model=dict, status_code=200)
#def login(user: User):
#    if user.email == "admin@gmail.com" and user.password == "admin":
#        token: str = create_token(user.dict())
#        return JSONResponse(status_code=200, content=token)


auth_router.post('/auth/register', tags=['auth'], response_model=dict, status_code=201)
def registration(user: User)->dict: 
    db = Session()
    # UserModel(name=user.name,password=user.password,active=user.active)
    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()

    return JSONResponse(status_code=201, content={"message": "Register Successfully"})
