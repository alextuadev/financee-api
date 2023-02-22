from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from config.jwt_manager import create_token, validate_token
from fastapi.responses import JSONResponse
from config.database import Session, engine, Base
from models.user import User as UserModel
from pydantic import BaseModel, Field
from fastapi.security import HTTPBearer


app = FastAPI()
app.version = "0.0.2"
app.title = "Finance API"

Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")


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

    
@app.get('/')
def message():
    return "Hello Financee API"


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


@app.post('/auth/register', tags=['users'], response_model=dict, status_code=201)
def registration(user: User)->dict: 
    db = Session()
    # UserModel(name=user.name,password=user.password,active=user.active)
    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()

    return JSONResponse(status_code=201, content={"message": "Register Successfully"})
