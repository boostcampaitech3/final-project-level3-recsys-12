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
    db: Session = Depends(get_db)) -> User:
    try:
        token: str = request.cookies.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        token_data = TokenData(username=username)
    except:
        # token decoding 실패 시
        return False
    user = get_user(db, id=token_data.username)
    if user is None:
        # DB에 유저가 없을 때
        return False
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is False:
        # token으로 user를 가져올 수 없을 때: decoding 실패 또는 DB에 유저 없음
        return False
    else:
        if current_user.disabled:
            # user가 휴면계정 상태일 때
            raise False
        return current_user