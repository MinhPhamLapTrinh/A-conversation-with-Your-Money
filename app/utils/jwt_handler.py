import jwt
from app.config import settings
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import HTTPException, Header

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# Password hasing
pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_backend_token(id: str, expires_in: int = 3600):
    """
    Generate a JWT token for backend functionalities
    :param id: User ID stored in DB
    :param expires_in: Token validity period in seconds (default: 1 hour)
    :return: Encoded JWT token
    """

    issued = datetime.now(timezone.utc)
    expiration = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    payload = {"sub": id, "exp": expiration}

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"token": token, "issued_at": issued, "exp": expiration}


def jwt_required(authorization: str = Header(None, alias="Authorization")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Authorization token missing or invalid"
        )

    token = authorization.split(" ")[1]
    return validate_backend_token(token=token)


def validate_backend_token(token: str):
    """
    Validate the JWT token.
    :param token: the JWT token from the Authorization header.
    :return: Decoded payload if valid.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
