from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from config.database import Base

class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True)
    bank_name = Column(String)
    icon = Column(String(180))
    is_active = Column(Boolean, default=True)
