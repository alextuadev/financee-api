from models.transaction import Transaction as TransactionModel
from sqlalchemy.orm import Session, mapper
from models.user import User
from models.transaction import Transaction

class TransactionService:
    
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_transactions(self):
        result = self.db.query(TransactionModel).all()
        return result

    def get_transaction(self, id):
        result = self.db.query(TransactionModel).filter(TransactionModel.id == id).first()
        return result