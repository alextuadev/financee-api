from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import Session
from schemas.user import User
from services.user import UserService


auth_router = APIRouter()

#auth_router.post('/auth/login', tags=['auth'], response_model=dict, status_code=200)
#def login(user: User):
#    if user.email == "admin@gmail.com" and user.password == "admin":
#        token: str = create_token(user.dict())
#        return JSONResponse(status_code=200, content=token)


@auth_router.post('/auth/register', tags=['auth'], response_model=dict, status_code=201)
def registration(user: User)->dict: 
    db = Session()  
    UserService(db).register(user)
    return JSONResponse(status_code=201, content={"message": "Register Successfully"})