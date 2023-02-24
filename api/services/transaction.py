from models.transaction import Transaction as TransactionModel
from sqlalchemy.orm import Session
from schemas.transaction import Transaction

class TransactionService:
    
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_transactions(self):
        result = self.db.query(TransactionModel).all()
        return result

    def get_transaction(self, id):
        result = self.db.query(TransactionModel).filter(TransactionModel.id == id).first()
        return result

    def get_transaction_by_category(self, category_id):
        result = self.db.query(TransactionModel).filter(TransactionModel.category_id == category_id).all()
        return result

    def get_transaction_by_user(self, user_id):
        result = self.db.query(TransactionModel).filter(TransactionModel.user_id == user_id).all()
        return result

    def create_transaction(self, transaction: Transaction):
        new_transaction = TransactionModel(**transaction.dict())
        self.db.add(new_transaction)
        self.db.commit()
        return

    def update_transaction(self, id: int, data: Transaction):
        transaction = self.db.query(TransactionModel).filter(TransactionModel.id == id).first()
        transaction.user_id = data.user_id
        transaction.category_id = data.category_id
        transaction.amount = data.amount
        transaction.date = data.date
        transaction.description = data.description
        self.db.commit()
        return