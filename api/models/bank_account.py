from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from config.database import Base
from models.user import User
from models.bank import Bank
from enum import Enum


class AccountType(Enum):
    Checking = "checking"
    Saving = "saving"

class BankAccount(Base):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True)
    account_name = Column(String)
    account_number = Column(String)
    label_name = Column(String)
    account_type = Column(SQLAlchemyEnum(AccountType), nullable=False)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bank_id = Column(Integer, ForeignKey('banks.id'))

    user = relationship(User, back_populates="bank_accounts")
    bank = relationship(Bank, back_populates="bank_accounts")