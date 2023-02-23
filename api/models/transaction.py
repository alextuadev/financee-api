from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    date = Column(DateTime, default=func.now())
    description = Column(String(500))
    amount = Column(Float)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")