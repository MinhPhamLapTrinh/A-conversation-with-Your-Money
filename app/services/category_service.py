from app.models.db.category_db import Category
from app.db.session import SessionDep
from sqlmodel import select
from fastapi import HTTPException


async def get_category(category_name: str, user_id: str, session: SessionDep):
    """
    Get category details by its name and type
    :param category_name: A category name of a transaction (rent, food, salary, and so on)
    :param user_id: A unique identifier for a user.
    :return a category stored db or NONE if the category isn't in db
    """

    try:
        category = session.exec(
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.name == category_name)
        ).first()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving category in db: {e}",
        )

    return category

async def get_category_by_id(id: str, user_id: str, session: SessionDep):
    """
    Get category details by its name and type
    :param id: A category ID
    :param user_id: A unique identifier for a user.
    :return a category stored db or NONE if the category isn't in db
    """

    try:
        category = session.exec(
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.category_id == id)
        ).first()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving category in db: {e}",
        )

    return category

async def add_category(
    user_id: str, category_name: str, category_type: str, session: SessionDep
):
    """
    Add a new category by its name and type
    :param user_id: A unique identifier for a user.
    :param category_name: A category name of a transaction (rent, food, salary, and so on)
    :param category_type: Income or Expense
    :return a created category in db
    """

    # Create new category in db
    try:
        category = Category(user_id=user_id, name=category_name, type=category_type)

        session.add(category)
        session.commit()
        session.refresh(category)

        return category
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while creating a new category in db: {e}",
        )
