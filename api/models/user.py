from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name =Column(String(150))
    email = Column(String(100), unique=True, index=True)
    password =Column(String(255))
    email_confirmation_at = Column(DateTime)
    active =Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="user")