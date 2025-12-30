from fastapi import APIRouter, HTTPException
from app.utils.jwt_handler import (
    get_password_hash,
    verify_password,
    create_backend_token,
    jwt_required,
)
from app.models.api.user import UserCreate, UserResponse
from app.db.session import SessionDep
from app.services.user_service import (
    get_user_by_email_from_db,
    create_user_in_db,
    get_user_by_username_from_db,
)

# Define router
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, session: SessionDep):
    """
    Allow users to register themselves to the app (username and user email must be unique)
    :param user_data: User information including password, username, user email
    :param session: A workspace for interacting with db
    :return 201: A successful message indicates that the user's information is saved in the db
    """

    # Check if their username is already registered
    existing_username = await get_user_by_username_from_db(user_data.username, session)
    if existing_username:
        raise HTTPException(
            status_code=400, detail=f"{existing_username.username} already registered"
        )

    # Check if they already registered by using the email
    existing_email = await get_user_by_email_from_db(user_data.user_email, session)
    if existing_email:
        raise HTTPException(
            status_code=400, detail=f"{existing_email.user_email} already registered"
        )

    # Hash the input password
    try:
        hashed_password = get_password_hash(user_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occurred while hashing the password: {e}"
        )

    # Create new user into a db
    user = await create_user_in_db(
        user_data.username, user_data.user_email, hashed_password, session
    )

    return {"status": "success", "user": user}
