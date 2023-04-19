from pydantic import BaseModel
from typing import Optional
from datetime import date

class Debt(BaseModel):
    to_whom: str
    description: str
    initial_amount: float
    current_amount_due: float
    monthly_payment: float
    interest_type: str
    annual_rate: float
    estimated_end_date: date
    reason: str
    bank_id: Optional[int]
    debt_type_id: int

    class Config:
        schema_extra = {
            "example": {
                "to_whom": "John Doe",
                "description": "Personal loan",
                "initial_amount": 10000,
                "current_amount_due": 9500,
                "initial_amount": 5000,
                "monthly_payment": 350,
                "interest_type": "saldos",
                "annual_rate": 12.0,
                "estimated_end_date": "2023-10-01",
                "reason": "Home renovation",
                "bank_id": 1,
                "debt_type_id": 1,
            }
        }