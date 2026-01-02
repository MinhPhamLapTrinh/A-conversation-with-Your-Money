from app.models.db.user_db import User
from app.db.session import SessionDep
from sqlmodel import select
from fastapi import HTTPException


async def get_user_by_email_from_db(email: str, session: SessionDep):
    """
    Get user information by their input email
    :param email: User email
    :param session: A workspace for interacting with db
    """
    try:
        existing_email = session.exec(
            select(User).where(User.user_email == email)
        ).first()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving user's email in db: {e}",
        )
    return existing_email


async def get_user_by_username_from_db(username: str, session: SessionDep):
    """
    Get user information by their input username
    :param username: User username
    :param session: A workspace for interacting with db
    """
    try:
        existing_username = session.exec(
            select(User).where(User.username == username)
        ).first()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving user's username in db: {e}",
        )
  
    return existing_username

async def get_user_by_user_id_from_db(user_id: str, session: SessionDep):
    """
    Get user information by their input user_id
    :param user_id: User user_id
    :param session: A workspace for interacting with db
    """
    try:
        user_id = session.exec(
            select(User).where(User.user_id == user_id)
        ).first()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while retrieving user's user_id in db: {e}",
        )
    return user_id

async def create_user_in_db(
    username: str, user_email: str, password: str, session: SessionDep
):
    """
    Creating a new user in db
    :param username: Username of a user
    :param user_email: user's email
    :password: A hashed password
    :param session: A workspace for interacting with db
    """
    # Create new user into a db
    try:
        user = User(
            username=username,
            user_email=user_email,
            hashed_password=password,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while creating a new user in db: {e}",
        )