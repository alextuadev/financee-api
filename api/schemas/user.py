
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class User(BaseModel):
    name:str = Field(min_length=5, max_length=150)
    email:str = Field(min_length=5, max_length=150)
    password:str = Field(min_length=8, max_length=150)
    email_confirmation_at: Optional[datetime] = None
    active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "name": "User name",
                "email": "email@email.com",
                "password": "123456789",
                "active": True
            }
        }

class UserLogin(BaseModel):
    email:str = Field(min_length=5, max_length=150)
    password:str = Field(min_length=8, max_length=150)
    class Config:
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "password": "123456789"       
            }
        }
