from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from models.bank_account import BankAccount as BankAccountModel
from schemas.bank_account import BankAccount


class BankAccountService:
    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_bank_accounts(self):
        stmt = select(BankAccountModel).options(joinedload(BankAccountModel.bank)).options(joinedload(BankAccountModel.user))

        result = await self.db.execute(stmt)
        bank_accounts = result.scalars().all()

        bank_accounts_without_passwords = []

        for account in bank_accounts:
            account_dict = account.__dict__
            # create a object copy without the password
            user_dict = account.user.__dict__.copy()
            user_dict.pop("password", None)
            account_dict["user"] = user_dict

            bank_accounts_without_passwords.append(account_dict)

        return bank_accounts_without_passwords

    async def get_bank_account(self, id):
        stmt = select(BankAccountModel).where(BankAccountModel.id == id)
        result = await self.db.execute(stmt)
        bank = result.scalar_one_or_none()

        return bank
       

    async def create_bank_account(self, bank: BankAccount):
        new_bank = BankAccountModel(**bank.dict())
        self.db.add(new_bank)

        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating bank account")
        
        return {"id": new_bank.id, "name": new_bank.account_name}

    
    async def update_bank_account(self, id: int, data: BankAccount):
        stmt = select(BankAccountModel).where(BankAccountModel.id == id)
        result = await self.db.execute(stmt)
        existing_bank = result.scalar_one_or_none()

        if existing_bank is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found")

        for key, value in data.dict().items():
            if value is not None:
                setattr(existing_bank, key, value)

        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating bank account")

        return existing_bank
    
    
    async def delete_bank_account(self, id: int) -> bool:
        stmt = delete(BankAccountModel).where(BankAccountModel.id == id)
        result = await self.db.execute(stmt)

        if result.rowcount == 0:
            return False

        await self.db.commit()
        return True