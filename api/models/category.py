from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    icon = Column(String(50))
    description = Column(String(500))

    transactions = relationship("Transaction", back_populates="category")