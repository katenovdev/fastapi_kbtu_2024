from fastapi import HTTPException, Request
import jwt 
from jwt import DecodeError, ExpiredSignatureError
from app.config.config import SECRET_KEY


ALGORITHM = "HS256"

async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_cookie = request.cookies.get("auth")
    if token_cookie is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token_cookie, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        if id is None:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    return id
