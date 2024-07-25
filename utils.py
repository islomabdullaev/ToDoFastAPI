from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from general import tashkent_tz

from general import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return bcrypt_context.hash(password)

def create_access_token(username: str, user_id: int):
    expires = datetime.now(tz=tashkent_tz) + timedelta(minutes=5)
    encode = {
        "sub": username,
        "id": user_id,
        "exp": expires}
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError as e:
        # Handle JWT decoding errors
        print(f"Error decoding token: {e}")
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(token=jwtoken)
        except Exception as e:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid