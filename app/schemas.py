from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class OperationCreate(BaseModel):
    operation_type: OperationType
    amount: float = Field(gt=0)


class WalletResponce(BaseModel):
    id: uuid.UUID
    balance: float
    created_at: str

    model_config = ConfigDict(from_attributes=True)


