from fastapi import APIRouter, HTTPException, Depends
from app.utils.jwt_handler import (
    get_password_hash,
    verify_password,
    create_backend_token,
    jwt_required,
)
from app.models.api.user import UserCreate, UserResponse, UserLogin
from app.db.session import SessionDep
from app.services.user_service import (
    get_user_by_email_from_db,
    create_user_in_db,
    get_user_by_username_from_db,
    get_user_by_user_id_from_db)

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


@router.post("/login", status_code=201)
async def login(credentials: UserLogin, session: SessionDep):
    """
    Allow users to login to their account
    :param credentials: A user email and password which are already registered
    :param session: A workspace for interacting with db
    :return 201: A successful message indicates that the user is authenticated
    """
    # Fetch the stored user in db
    user = await get_user_by_email_from_db(credentials.email, session)

    # Compare the input password with the hashed password stored in db
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail=f"Invalid Email or Password! Please try again!"
        )

    # Generate backend token
    backend_token = create_backend_token(id=str(user.user_id))

    return {
        "status": "success",
        "user_id": user.user_id,
        "token": backend_token["token"],
        "issued_at": backend_token["issued_at"],
        "expires_in": backend_token["exp"],
    }


@router.get("/profile", status_code=200, response_model=UserResponse)
async def get_profile(session: SessionDep, payload: dict = Depends(jwt_required)):
    """
    Validate the given token
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :return success message and information of user which is extracted from token
    """

    # Get user id from the payload
    user_id = payload.get("sub")

    # Retrieve user information from db using user_id
    user = await get_user_by_user_id_from_db(user_id, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    return {"status": "success", "user": user}
