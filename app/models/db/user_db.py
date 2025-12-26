from api.user import UserBase
from sqlmodel import Field
from uuid import UUID, uuid5 
from datetime import datetime, timezone
class User(UserBase, table=True):
    # Primary Key
    user_id: UUID = Field(default_factory= uuid5, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = datetime.now(timezone.utc)
    