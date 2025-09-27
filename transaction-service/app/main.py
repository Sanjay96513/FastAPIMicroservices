from fastapi import FastAPI, Depends, HTTPException, status, Request
from beanie import PydanticObjectId

from shared_lib.database import init_db
from shared_lib.models import Transaction, User

app = FastAPI(
    title="Transaction Processing Service",
    description="Processes financial transactions, including transfers and payments.",
    version="0.1.0"
)

# This is a simplified dependency to simulate getting the user ID
# from the API Gateway after it has authenticated the user.
# In a real-world scenario, the gateway would validate the JWT
# and pass the user's ID in a header like this.
async def get_current_user_id(request: Request) -> PydanticObjectId:
    """
    A dependency that extracts the user ID from a request header.
    """
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in headers",
        )
    return PydanticObjectId(user_id)


@app.on_event("startup")
async def on_startup():
    """Initialize the database connection on startup."""
    await init_db()


@app.post("/transactions/", response_model=Transaction)
async def create_transaction(
    transaction_in: Transaction,
    sender_id: PydanticObjectId = Depends(get_current_user_id)
):
    """
    Creates a new financial transaction.

    The sender ID is automatically inferred from the authenticated user.
    """
    # Ensure the sender from the token is the one in the transaction
    if sender_id != transaction_in.sender_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sender ID does not match authenticated user.",
        )

    # In a real app, you would validate the receiver_id, check balances, etc.
    await transaction_in.insert()

    # Here you could trigger a call to the risk-service for analysis
    # e.g., using httpx.post("http://risk-service:8000/analyze", json=transaction.dict())

    return transaction_in


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "transaction-service"}