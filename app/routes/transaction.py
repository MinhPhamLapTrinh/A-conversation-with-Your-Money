from fastapi import APIRouter, HTTPException, Depends
from app.models.api.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionRead,
    TransactionUpdate,
)
from app.db.session import SessionDep
from app.utils.jwt_handler import jwt_required
from app.services.category_service import get_category, add_category, get_category_by_id
from app.services.transaction_service import (
    add_transaction,
    get_list_transactions,
    get_transaction_by_id,
    remove_transaction,
    update_transaction_in_db,
)

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
        category_type=category.type,
    )

    return {"status": "success", "transaction": transaction_read}


@router.get("/transactions", status_code=200)
async def list_transactions(session: SessionDep, payload: dict = Depends(jwt_required)):
    """
    Allow users to retrieve the list of transactions that they made
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :param session: A workspace for interacting with db
    :return a successful message with the list of transactions stored in db
    """
    # Get user id from the payload
    user_id = payload.get("sub")

    transactions = await get_list_transactions(user_id=user_id, session=session)

    if not transactions:
        raise HTTPException(status_code=404, detail=f"List is empty!")

    # Format transactions with category information
    transactions_list = []
    for transaction in transactions:
        category = await get_category_by_id(
            id=transaction.category_id, user_id=user_id, session=session
        )
        transaction_dict = {
            "transaction_id": str(transaction.transaction_id),
            "category_id": str(transaction.category_id),
            "amount": transaction.amount,
            "direction": transaction.direction,
            "description": transaction.description,
            "occurred_at": transaction.occurred_at,
            "created_at": transaction.created_at,
            "category_name": category.name,
            "category_type": category.type,
        }
        transactions_list.append(transaction_dict)

    return {"status": "success", "transactions": transactions_list}


@router.get("/transaction/{id}", status_code=200, response_model=TransactionResponse)
async def get_transaction(
    id: str, session: SessionDep, payload: dict = Depends(jwt_required)
):
    """
    Allow users to retrieve the transaction the given ID
    :param id: Transaction ID
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :param session: A workspace for interacting with db
    """

    # Get user id from the payload
    user_id = payload.get("sub")

    transaction = await get_transaction_by_id(
        transaction_id=str(id), user_id=user_id, session=session
    )

    if not transaction:
        raise HTTPException(status_code=404, detail=f"There is no {id} transaction")

    # Retrieve category details
    category = await get_category_by_id(
        id=transaction.category_id, user_id=user_id, session=session
    )

    if not category:
        raise HTTPException(status_code=404, detail=f"There is no available category")

    return {
        "status": "success",
        "transaction": {
            "transaction_id": str(transaction.transaction_id),
            "category_id": str(transaction.category_id),
            "amount": transaction.amount,
            "direction": transaction.direction,
            "description": transaction.description,
            "occurred_at": transaction.occurred_at,
            "created_at": transaction.created_at,
            "category_name": category.name,
            "category_type": category.type,
        },
    }


@router.delete("/transaction/{id}", status_code=200)
async def delete_transaction(
    id: str, session: SessionDep, payload: dict = Depends(jwt_required)
):
    """
    Allow users to remove a transaction
    :param id: Transaction ID
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :param session: A workspace for interacting with db
    """

    # Get user id from the payload
    user_id = payload.get("sub")

    # Retrieve a transaction
    transaction = await get_transaction_by_id(
        transaction_id=str(id), user_id=user_id, session=session
    )

    if not transaction:
        raise HTTPException(status_code=404, detail=f"There is no {id} transaction")

    # Remove a transaction
    await remove_transaction(transaction_id=id, user_id=user_id, session=session)

    return {"status": "success", "msg": "The transaction is removed"}


@router.patch("/transaction/{id}", status_code=200, response_model=TransactionResponse)
async def update_transaction(
    id: str,
    data: TransactionUpdate,
    session: SessionDep,
    payload: dict = Depends(jwt_required),
):
    """
    Allow users to update their transaction
    :param id: Transaction ID
    :param data: New updated data
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :param session: A workspace for interacting with db
    """

    # Get user id from the payload
    user_id = payload.get("sub")

    transaction = await update_transaction_in_db(
        transaction_id=id, user_id=user_id, data=data, session=session
    )

    # Retrieve category details
    category = await get_category_by_id(
        id=transaction.category_id, user_id=user_id, session=session
    )

    return {
        "status": "success",
        "transaction": {
            "transaction_id": str(transaction.transaction_id),
            "category_id": str(transaction.category_id),
            "amount": transaction.amount,
            "direction": transaction.direction,
            "description": transaction.description,
            "occurred_at": transaction.occurred_at,
            "created_at": transaction.created_at,
            "category_name": category.name,
            "category_type": category.type,
        },
    }
