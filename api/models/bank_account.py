from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from config.database import Base
from models.user import User
from enum import Enum


class AccountType(Enum):
    Checking = "checking"
    Saving = "saving"

class BankAccount(Base):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True)
    bank_name = Column(String)
    account_number = Column(String)
    account_type = Column(SQLAlchemyEnum(AccountType), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship(User, back_populates="bank_accounts")