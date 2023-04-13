from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from config.database import Base


class CreditCard(Base):
    __tablename__ = 'credit_cards'

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(16), unique=True, index=True)
    cardholder_name = Column(String(150))
    expiry_date = Column(Date)
    category_card = Column(String(150), nullable=True)
    card_type = Column(String(20), nullable=True)
    payment_due_date = Column(Date, nullable=True)
    statement_date = Column(Date, nullable=True)
    is_active = Column(Integer, default=1)
    is_owner = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey('users.id'))
    bank_id = Column(Integer, ForeignKey('banks.id'))

    user = relationship("User", back_populates="credit_cards")
    bank = relationship("Bank", back_populates="credit_cards")

