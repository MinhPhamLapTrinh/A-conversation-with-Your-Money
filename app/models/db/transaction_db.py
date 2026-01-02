from app.models.api.transaction import TransactionBase
from sqlmodel import Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, Literal

class Transaction(TransactionBase, table=True):
    __tablename__ = "transactions"

    # Primary Key
    transaction_id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id : UUID = Field(foreign_key="users.user_id", index=True)
    category_id: UUID = Field(foreign_key="categories.category_id", index=True)

    amount: float
    # Income is "in", expense is "out"
    direction   : str = Field(index=True) 

    description: Optional[str]
    occurred_at: datetime

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

