from pydantic import BaseModel


class Bank(BaseModel):
    bank_name: str
    icon: str
    is_active: bool
        
    class Config:
        schema_extra = {
            "example": {
                "bank_name": "Banco Industrial",
                "icon": "banco.png",
                "is_active": True,
            }
        }
   