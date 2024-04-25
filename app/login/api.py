from datetime import datetime
from typing import List
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
import jwt
import jwt.exceptions
from pydantic import BaseModel
from requests import request
from sqlalchemy.orm import Session
from app.constent import ALGORITHM, SECRET_KEY
from app.models import User
from database import get_db
from starlette import status
from datetime import datetime, timedelta

loginroute = APIRouter(prefix="/login")


@loginroute.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: dict,
    db: Session = Depends(get_db),
):
    """
    Creates a new user or returns a token for an existing user.

    Args:
        request (dict): User data, including email (optional) and id (optional for Google OAuth).
        db (Session): Database session dependency.

    Returns:
        dict:
            - token (str, optional): Access token for an existing user.
            - error (str, optional): Error message if user creation fails.
    """

    # Validate request data
    if request.get("email") is None and request.get("id") is None:
        raise ValueError("Missing email and Google ID for user creation.")

    # Efficiently check for existing user (combine email and ID check)
    existing_user = (
        db.query(User)
        .filter(
            User.email == request.get("email") or User.google_id == request.get("id")
        )
        .first()
    )

    if existing_user:
        return {"token": create_access_token(existing_user.email, existing_user.id)}

    # Create new user with data extraction for clarity
    try:
        user_data = {
            "email": request.get("email"),
            "google_id": request.get("id"),
            "name": request.get("name"),
            "created_by_id": 1,  # Assuming created_by_id is always 1
        }
        user = User(**user_data)
        db.add(user)
        db.commit()

        # Retrieve newly created user (avoid redundant query)
        new_user = user

        return {"token": create_access_token(new_user.email, new_user.id)}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def create_access_token(data: dict, id, expires_delta: timedelta = None):
    to_encode = {"email": data, "id": id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
