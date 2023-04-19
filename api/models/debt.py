from config.database import Base
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship


class Debt(Base):
    __tablename__ = 'debts'

    id = Column(Integer, primary_key=True, index=True)
    to_whom = Column(String(200), nullable=False)
    description = Column(String(350), nullable=True)
    initial_amount = Column(Numeric, nullable=True)
    current_amount_due = Column(Numeric, nullable=True)
    monthly_payment = Column(Numeric, nullable=False)
    interest_type = Column(String(50), nullable=False) 
    annual_rate = Column(Numeric, nullable=False)
    estimated_end_date = Column(Date, nullable=False)
    reason = Column(String(255), nullable=True)

    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    debt_type_id = Column(Integer, ForeignKey('debt_types.id'), nullable=False)

    debt_type = relationship("DebtType", back_populates="debts")
    bank = relationship("Bank", back_populates="debts")
    user = relationship("User", back_populates="debts")