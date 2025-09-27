from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User(Document):
    """
    Represents a user in the database.
    """
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users" # MongoDB collection name

class Transaction(Document):
    """
    Represents a financial transaction.
    """
    amount: float = Field(..., gt=0)
    description: str
    sender_id: PydanticObjectId
    receiver_id: PydanticObjectId
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "transactions"

# Pydantic models for request/response bodies (not stored in DB)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str