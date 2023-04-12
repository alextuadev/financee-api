from pydantic import BaseModel
from datetime import date
from typing import Optional


class CreditCard(BaseModel):
    card_number: str
    category_card: str
    card_type: str
    cardholder_name: str
    expiry_date: date
    payment_due_date: Optional[date] = None
    statement_date: Optional[date] = None
    is_active: bool
    is_owner: bool

    class Config:
        schema_extra = {
            "example": {
                "card_number": "1111",
                "cardholder_name": "John Doe",
                "card_type": "Visa",
                "category_card": "Oro",
                "expiry_date": "2025-12-31",
                "payment_due_date": "2023-05-15",
                "statement_date": "2023-05-01",
                "is_active": True,
                "is_owner": True
            }
        }