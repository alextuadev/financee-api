from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

from models.debt import Debt as DebtModel
from schemas.debt import Debt


class DebtService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_debt(self, debt: Debt, user_id: int):
        new_debt = DebtModel(**debt.dict(), user_id=user_id)
        self.db.add(new_debt)
        await self.db.commit()

        return new_debt

    async def get_debts(self, user_id: int):
        stmt = select(DebtModel).options(joinedload(DebtModel.debt_type)).where(DebtModel.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_debt(self, id: int, user_id: int):
        stmt = select(DebtModel).options(joinedload(DebtModel.debt_type)).where(DebtModel.user_id == user_id, DebtModel.id == id)
        result = await self.db.execute(stmt)
        debt = result.scalar_one_or_none()
        if debt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")
        return debt

    async def update_debt(self, id: int, debt: Debt, user_id: int):
        stmt = select(DebtModel).where(DebtModel.user_id == user_id, DebtModel.id == id)
        result = await self.db.execute(stmt)
        existing_debt = result.scalar_one_or_none()

        if existing_debt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")

        existing_debt.update(**debt.dict())
        await self.db.commit()

    async def delete_debt(self, id: int, user_id: int):
        stmt = select(DebtModel).where(DebtModel.user_id == user_id, DebtModel.id == id)
        result = await self.db.execute(stmt)
        existing_debt = result.scalar_one_or_none()

        if existing_debt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")

        await self.db.delete(existing_debt)
        await self.db.commit()