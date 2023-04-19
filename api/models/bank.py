from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from config.database import Base

class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True)
    bank_name = Column(String)
    icon = Column(String(180))
    is_active = Column(Boolean, default=True)

    bank_accounts = relationship("BankAccount", back_populates="bank")
    credit_cards = relationship("CreditCard", back_populates="bank")
    debts = relationship("Debt", back_populates="bank")
