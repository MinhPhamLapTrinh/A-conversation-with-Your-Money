from app.models.db.transaction_db import Transaction
from app.db.session import SessionDep
from sqlmodel import select
from fastapi import HTTPException
from app.utils.time_converter import convert_string_time_to_iso


async def add_transaction(
    user_id: str,
    category_id: str,
    amount: float,
    direction: str,
    occurred_at: str,
    session: SessionDep,
    description: str | None = None,
):
    """
    Add a new transaction to db
    :param user_id: A unique identifier for a user.
    :param category_id: An ID of a category
    :param amount: the user input amount
    :param direction: In if it's an income or Out if it's an expense
    :param occurred_at: The time that they make that transaction
    :param session: A workspace for interacting with db
    :description: A quick note for that transaction or NONE
    :return a created transaction in db
    """
    date = convert_string_time_to_iso(str(occurred_at))
    # Create new transaction in db
    try:
        transaction = Transaction(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            direction=direction,
            occurred_at=date,
            description=description,
        )

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return transaction
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while creating a new transaction in db: {e}",
        )


async def get_list_transactions(user_id: str, session: SessionDep):
    """
    Retrieve a list of transactions
    :param user_id: A unique identifier for a user
    :param session: A workspace for interacting with db
    """

    try:
        transactions = session.exec(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.occurred_at.desc())
        ).all()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving the list of transactions: {e}",
        )

    return transactions


async def get_transaction_by_id(transaction_id: str, user_id: str, session: SessionDep):
    """
    Retrieve a transaction by ID
    :param transaction_id: Transaction ID
    :param user_id: A unique identifier for a user
    :param session: A workspace for interacting with db
    """

    try:
        transaction = session.exec(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .where(Transaction.transaction_id == transaction_id)
        ).first()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving the {transaction_id} transaction: {e}",
        )

    return transaction