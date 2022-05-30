import os
from fastapi import Request, HTTPException, status, Depends

from db.database import SessionLocal
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from db.schemas import User, TokenData
from db.crud import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from db.crud import get_user

base_dir = os.path.abspath(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, 'templates'))

# Dependency
# 오류가 나도 session은 닫자!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    request: Request,
    db : Session = Depends(get_db)) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token: str = request.cookies.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, id=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user