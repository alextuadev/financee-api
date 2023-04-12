import os
from schemas.user import User
from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from pydantic import BaseModel
from models.user import User as UserModel
from passlib.context import CryptContext
from jose import jwt
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET=os.environ.get("SECRET_KEY", "")
JWT_ALGORITHM = "HS256"

class UserService():
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register(self, user: User):
        # Verificar si el usuario ya existe en la base de datos
        stmt = select(UserModel).where(UserModel.email == user.email)
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()
    
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email is already registered")

        # Hashear la contraseña del usuario
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password

        # Crear un nuevo objeto User con los datos de entrada
        new_user = UserModel(**user.dict())

        # Agregar el nuevo usuario a la sesión de la base de datos
        self.db.add(new_user)


        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
       
        return {"id": new_user.id, "email": new_user.email}
    

    async def token(self, user: User):
        stmt = select(UserModel).where(UserModel.email == user.email)
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password 404")
        
        if pwd_context.verify(user.password, existing_user.password):
            token = jwt.encode({"user_id": existing_user.id, "username": existing_user.email}, JWT_SECRET, algorithm=JWT_ALGORITHM)
            
            # Convert the existing_user object to a dictionary and remove the 'password' key
            user_data = existing_user.__dict__.copy()
            user_data.pop("password", None)
            user_data.pop("email_confirmation_at", None)

            return {"access_token": token, "token_type": "bearer", "user": jsonable_encoder(user_data)}
        else:
            return {"message": "Invalid username or password"}