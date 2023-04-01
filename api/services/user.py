import os
from schemas.user import User
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from pydantic import BaseModel
from models.user import User as UserModel
from passlib.context import CryptContext
from jose import jwt
from fastapi.encoders import jsonable_encoder

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET=os.environ.get("SECRET_KEY", "")
JWT_ALGORITHM = "HS256"

class UserService():
    def __init__(self, db: Session) -> None:
        self.db = db

    def register(self, user: User):
        # Verificar si el usuario ya existe en la base de datos
        if self.db.query(UserModel).filter(UserModel.email == user.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email is already registered")
   
        # Hashear la contraseña del usuario
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password

        # Crear un nuevo objeto User con los datos de entrada
        new_user = UserModel(**user.dict())

        # Agregar el nuevo usuario a la sesión de la base de datos
        self.db.add(new_user)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
        
        return {"id": new_user.id, "email": new_user.email}
    

    def token(self, user: User):
        existUser = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        if existUser is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password 404")
        
        if pwd_context.verify(user.password, existUser.password):
            token = jwt.encode({"username": user.email}, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return {"access_token": token, "token_type": "bearer", "user": jsonable_encoder(existUser)}
        else:
            return {"message": "Invalid username or password"}