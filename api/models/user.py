from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name =Column(String(150))
    email =Column(String(150))
    password =Column(String(255))
    active =Column(Boolean)