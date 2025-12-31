from app.models.api.category import CategoryBase
from sqlmodel import Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    # Primary Key
    category_id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id : UUID = Field(foreign_key="user_id", index=True)

    # Category details
    name: str = Field(index=True)
    type: str = Field(index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))