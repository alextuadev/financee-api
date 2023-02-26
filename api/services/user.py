from schemas.user import User
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from pydantic import BaseModel
from models.user import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        
        # Devolver los datos del usuario recién creado
        return {"id": new_user.id, "email": new_user.email}