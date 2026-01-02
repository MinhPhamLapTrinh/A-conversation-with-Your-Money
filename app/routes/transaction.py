from fastapi import APIRouter, HTTPException, Depends
from app.models.api.transaction import TransactionCreate, TransactionResponse, TransactionRead
from app.db.session import SessionDep
from app.utils.jwt_handler import jwt_required
from app.services.category_service import get_category, add_category
from app.services.transaction_service import add_transaction

# Define router
router = APIRouter()


@router.post("/transaction", status_code=201, response_model=TransactionResponse)
async def create_transaction(
    data: TransactionCreate, session: SessionDep, payload: dict = Depends(jwt_required)
):
    """
    Allow users to record the transaction
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :param data: Detail of a transaction
    :param session: A workspace for interacting with db
    :return a successful message indicates that the transaction is posted
    """

    # Validate the amount
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0!")

    # In for income and Out for Expense
    direction = "in" if data.category_type == "income" else "out"

    # Get user id from the payload
    user_id = payload.get("sub")

    # Find or create category
    category = await get_category(
        category_name=data.category_name,
        user_id=user_id,
        session=session,
    )

    if not category:
        category = await add_category(
            user_id=user_id,
            category_name=data.category_name,
            category_type=data.category_type,
            session=session,
        )
    # Create transaction
    transaction = await add_transaction(
        user_id=user_id,
        category_id=category.category_id,
        amount=data.amount,
        direction=direction,
        occurred_at=data.occurred_at,
        session=session,
        description=data.description,
    )

    # Format response with category information
    transaction_read = TransactionRead(
        transaction_id=transaction.transaction_id,
        category_id=transaction.category_id,
        amount=transaction.amount,
        direction=transaction.direction,
        description=transaction.description,
        occurred_at=transaction.occurred_at,
        category_name=category.name,
        category_type=category.type
    )

    return {"status": "success", "transaction": transaction_read, "occurred_at": transaction.occurred_at}