from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID


class UserBase(SQLModel):
    username: str = Field(index=True)
    # Validate if the email is actually in the email format
    user_email: EmailStr = Field(index=True)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: UUID
    created_at: datetime

class UserResponse(SQLModel):
    status: str
    user: UserRead

class UserLogin(SQLModel):
    email: str
    password: str