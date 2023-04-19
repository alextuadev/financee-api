from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from models.debt_type import DebtType as DebtTypeModel
from schemas.debt_type import DebtTypeCreate, DebtTypeUpdate


class DebtTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_debt_type(self, debt_type: DebtTypeCreate):
        new_debt_type = DebtTypeModel(**debt_type.dict())
        self.db.add(new_debt_type)
        await self.db.commit()
        await self.db.refresh(new_debt_type)
        return new_debt_type

    async def get_debt_types(self):
        stmt = select(DebtTypeModel)
        result = await self.db.execute(stmt)
        debt_types = result.scalars().all()
        return debt_types

    async def get_debt_type(self, id: int):
        stmt = select(DebtTypeModel).where(DebtTypeModel.id == id)
        result = await self.db.execute(stmt)
        try:
            debt_type = result.scalar_one()
        except NoResultFound:
            return None
        return debt_type

    async def update_debt_type(self, id: int, debt_type: DebtTypeUpdate):
        stmt = update(DebtTypeModel).where(DebtTypeModel.id == id).values(**debt_type.dict()).returning(DebtTypeModel)
        result = await self.db.execute(stmt)
        try:
            updated_debt_type = result.scalar_one()
        except NoResultFound:
            return None
        await self.db.commit()
        return updated_debt_type

    async def delete_debt_type(self, id: int):
        stmt = delete(DebtTypeModel).where(DebtTypeModel.id == id).returning(DebtTypeModel)
        result = await self.db.execute(stmt)
        try:
            deleted_debt_type = result.scalar_one()
        except NoResultFound:
            return None
        await self.db.commit()
        return deleted_debt_type