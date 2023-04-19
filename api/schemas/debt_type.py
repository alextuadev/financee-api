# schemas/debt_type.py
from pydantic import BaseModel

class DebtTypeBase(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Extrafinanciamento",
            }
        }

class DebtTypeCreate(DebtTypeBase):
    pass

class DebtTypeUpdate(DebtTypeBase):
    pass

class DebtType(DebtTypeBase):
    id: int

    class Config:
        orm_mode = True