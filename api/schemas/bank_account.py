from pydantic import BaseModel


class BankAccount(BaseModel):
    account_name: str
    account_number: str
    label_name: str
    is_active: bool
    account_type: str
    user_id: int
    bank_id: int
        
    class Config:
        schema_extra = {
            "example": {
                "account_name": "Alexis",
                "account_number": "1234",
                "label_name": "Alexis",
                "is_active": True,
                "account_type": "checking",
                "user_id": 1,
                "bank_id": 1
            }
        }
   