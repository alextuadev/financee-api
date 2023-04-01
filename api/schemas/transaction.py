from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    user_id: int
    category_id: int
    date: str
    description: Optional[str] = None
    amount: float
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "category_id": 1,
                "date": "2021-03-01",
                "description": "Example description",
                "amount": 100.00
            }
        }
   