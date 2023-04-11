from fastapi import HTTPException,status
from models.bank import Bank as BankModel
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.bank import Bank
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete


class BankService:
    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_banks(self):
        stmt = select(BankModel)
        result = await self.db.execute(stmt)
        banks = result.scalars().all()

        return banks

    async def get_bank(self, id):
        stmt = select(BankModel).where(BankModel.id == id)
        result = await self.db.execute(stmt)
        bank = result.scalar_one_or_none()

        return bank
       

    async def create_bank(self, bank: Bank):
        new_bank = BankModel(**bank.dict())
        self.db.add(new_bank)

        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
        
        return {"id": new_bank.id, "name": new_bank.bank_name}

    
    async def update_bank(self, id: int, data: Bank):
        stmt = select(BankModel).where(BankModel.id == id)
        result = await self.db.execute(stmt)
        existing_bank = result.scalar_one_or_none()

        if existing_bank is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")

        for key, value in data.dict().items():
            if value is not None:
                setattr(existing_bank, key, value)

        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating bank")

        return existing_bank
    
    
    async def delete_bank(self, id: int) -> bool:
        stmt = delete(BankModel).where(BankModel.id == id)
        result = await self.db.execute(stmt)

        if result.rowcount == 0:
            return False

        await self.db.commit()
        return True