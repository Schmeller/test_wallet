from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from . import models, schemas
from decimal import Decimal


class WalletService:
    @staticmethod
    def get_wallet(db: Session, wallet_id: uuid.UUID):
        return db.execute(
            select(models.Wallet).where(models.Wallet.id == wallet_id)
        ).scalar_one_or_none()
    
    @staticmethod
    def create_wallet(db: Session):
        wallet = models.Wallet()
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet
    
    @staticmethod
    def process_operation(db: Session, wallet_id: uuid.UUID, operation: schemas.OperationCreate):
        wallet = db.execute(
            select(models.Wallet)
            .where(models.Wallet.id == wallet_id)
            .with_for_update()
        ).scalar_one_or_none()

        if not wallet:
            raise ValueError("Wallet not found")
        
        amount = Decimal(str(operation.amount))

        if operation.operation_type == schemas.OperationType.WITHDRAW:
            if wallet.balance < amount:
                raise ValueError("Insufficient funds")
            wallet.balance -= amount
        else:
            wallet.balance += amount
        
        operation_record = models.Operation(
            wallet_id=wallet_id,
            operation_type=operation.operation_type,
            amount=amount
        )
        db.add(operation_record)
        db.commit()
        db.refresh(wallet)

        return wallet
