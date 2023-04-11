from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from config.database import Base
from models.user import User
from enum import Enum


class CreditCard(Base):
    __tablename__ = 'credit_cards'
    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    
    expiration_date = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="credit_cards")