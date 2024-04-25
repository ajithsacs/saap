from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from grpc import Status
import jwt
import jwt.exceptions

from app.constent import ALGORITHM, SECRET_KEY


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        print("credentials", credentials)
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme."
            )

        user_data = self.verify_token(credentials.credentials)

        if user_data is False:
            raise HTTPException(
                status_code=401, detail="Invalid token or expired token."
            )

    async def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=Status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token format.",
                )
            return email
        except jwt.PyJWTError:
            print("Invalid token:", token)  # Log the invalid token for debugging
            raise HTTPException(
                status_code=Status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or expired token.",
            )
