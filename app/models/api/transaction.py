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
    description: Optional[str] = None

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


class TransactionUpdate(SQLModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None

    category_name: Optional[str] = None
    category_type: Optional[Literal["income", "expense"]] = None
    