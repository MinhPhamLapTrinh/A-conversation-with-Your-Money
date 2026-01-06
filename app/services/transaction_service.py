from app.models.db.transaction_db import Transaction
from app.models.db.category_db import Category
from app.db.session import SessionDep
from sqlmodel import select
from fastapi import HTTPException
from app.models.api.transaction import TransactionUpdate


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
    # Create new transaction in db
    try:
        transaction = Transaction(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            direction=direction,
            occurred_at=occurred_at,
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
    :return a list of transactions
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
    :return a transaction by its id
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


async def remove_transaction(transaction_id: str, user_id: str, session: SessionDep):
    """
    Remove a transaction by ID
    :param transaction_id: Transaction ID
    :param user_id: A unique identifier for a user
    :param session: A workspace for interacting with db
    :return a transaction is removed from db
    """

    try:
        transaction = session.exec(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .where(Transaction.transaction_id == transaction_id)
        ).first()

        session.delete(transaction)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error while removing the {transaction_id} transaction: {e}",
        )


async def update_transaction_in_db(
    transaction_id: str, user_id: str, data: TransactionUpdate, session: SessionDep
):
    """
    Update an existing transaction
    :param transaction_id: Transaction ID
    :param user_id: A unique identifier for a user
    :param data: New updated transaction
    :param session: A workspace for interacting with db
    :return an updated transaction
    """

    transaction = session.exec(
        select(Transaction)
        .where(Transaction.transaction_id == transaction_id)
        .where(Transaction.user_id == user_id)
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update amount
    if data.amount is not None:
        if data.amount <= 0:
            raise HTTPException(
                status_code=400, detail="Amount must be greater than zero!"
            )
        transaction.amount = data.amount

    # Update description
    if data.description is not None:
        transaction.description = data.description

    # Update occurred time
    if data.occurred_at is not None:
        transaction.occurred_at = data.occurred_at

    # Update category
    if data.category_name and data.category_type:
        category = session.exec(
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.name == data.category_name)
            .where(Category.type == data.category_type)
        ).first()

        if not category:
            category = Category(
                user_id=user_id,
                name=data.category_name,
                type=data.category_type,
            )
            session.add(category)
            session.commit()
            session.refresh(category)

        transaction.category_id = category.category_id

        # Direction stays deterministic
        transaction.direction = "in" if data.category_type == "income" else "out"

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction
