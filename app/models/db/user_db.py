from app.models.api.user import UserBase
from sqlmodel import Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


class User(UserBase, table=True):
    __tablename__ = "users"
    # Primary Key
    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
