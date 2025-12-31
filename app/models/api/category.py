from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID
from typing import Literal

class CategoryBase(SQLModel):
    # Name of the category (transportation, rent, salary, and ..)
    name: str = Field(index=True)
    type: Literal["income", "expense"] = Field(index=True) # Expense or Income
    user_id: UUID = Field(index=True)
    created_at: datetime
    