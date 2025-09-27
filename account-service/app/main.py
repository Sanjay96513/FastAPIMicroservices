from fastapi import FastAPI, HTTPException, status
from beanie import PydanticObjectId

from shared_lib.database import init_db
from shared_lib.models import User

app = FastAPI(
    title="Account Management Service",
    description="Manages user profiles, registration, and account settings.",
    version="0.1.0"
)

@app.on_event("startup")
async def on_startup():
    """Initialize the database connection on startup."""
    await init_db()

@app.get("/users/{user_id}", response_model=User)
async def get_user_profile(user_id: PydanticObjectId):
    """
    Retrieve a user's profile by their unique ID.

    In a real application, this endpoint should be protected and
    ensure the requester has the right permissions.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "account-service"}