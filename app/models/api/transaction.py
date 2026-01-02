from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, Literal

class TransactionBase(SQLModel):
    occurred_at: datetime = Field(index=True) 

class TransactionCreate(TransactionBase):
    category_name: str
    category_type: Literal["expense", "income"]
    amount: float
    occurred_at: datetime
    description: Optional[str]

class TransactionRead(TransactionBase):
    transaction_id: UUID
    category_id: UUID
    amount: float
    direction: str
    description: Optional[str]
    occurred_at: datetime
    category_name: str
    category_type: str

class TransactionResponse(SQLModel):
    status: str
    transaction: TransactionRead