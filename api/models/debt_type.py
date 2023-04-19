from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class DebtType(Base):
    __tablename__ = 'debt_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    debts = relationship("Debt", back_populates="debt_type")
