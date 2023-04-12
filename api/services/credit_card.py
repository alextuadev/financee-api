from fastapi import HTTPException,status
from models.credit_card import CreditCard as CreditCardModel
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.credit_card import CreditCard
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete


class CreditCardService:
    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_credit_cards(self, user_id: int):
        stmt = select(CreditCardModel).where(CreditCardModel.user_id == user_id)
        result = await self.db.execute(stmt)
        credit_cards = result.scalars().all()
        return credit_cards
    

    async def get_credit_card(self, credit_card_id: int, user_id: int):
        stmt = select(CreditCardModel).where(CreditCardModel.id == credit_card_id, CreditCardModel.user_id == user_id)
        result = await self.db.execute(stmt)
        credit_card = result.scalar()
        if credit_card is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit card not found")
        return credit_card


    async def create_credit_card(self, credit_card: CreditCard, user_id: int):
        new_credit_card = CreditCardModel(**credit_card.dict(), user_id=user_id)
        self.db.add(new_credit_card)

        try:
            await self.db.commit()
            await self.db.refresh(new_credit_card)
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating credit card")

        return new_credit_card

    
    async def update_credit_card(self, credit_card_id: int, credit_card_data: CreditCard, user_id: int):
        stmt = (
            update(CreditCardModel)
            .where(CreditCardModel.id == credit_card_id, CreditCardModel.user_id == user_id)
            .values(**credit_card_data.dict())
            .returning(CreditCardModel)
        )
        result = await self.db.execute(stmt)
        updated_credit_card = result.scalar()
        if updated_credit_card is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit card not found")
        return updated_credit_card

    
    
    async def delete_credit_card(self, credit_card_id: int, user_id: int):
        stmt = delete(CreditCardModel).where(CreditCardModel.id == credit_card_id, CreditCardModel.user_id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit card not found")
        return {"message": "Credit card deleted"}