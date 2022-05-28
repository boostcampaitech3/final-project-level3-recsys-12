# basic
from datetime import datetime, timedelta
import os

# fastapi
from fastapi import APIRouter, Form, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

# token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# defined objects
from utils import templates, get_db
from db.crud import get_user
from db.crud import pwd_context, SECRET_KEY, ALGORITHM, FAKE_PASSWORD
from db.schemas import UserCreate

# type hint
from sqlalchemy.orm import Session
from typing import Optional

ACCESS_TOKEN_EXPIRE_MINUTES = 30

login_router = APIRouter(prefix="/login")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# tokenURL: user가 token을 얻기 위해 id와 password를 send하는 곳.
#         : 상대적인 경로이다. ./login


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, to_login_user: UserCreate) -> bool:
    user = get_user(db, to_login_user.user_id)
    if not user:
        return False
    if not verify_password(to_login_user.password+FAKE_PASSWORD, user.hashed_password):
        return False
    return True


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@login_router.get("/")
def get_login_form(request: Request):
    return templates.TemplateResponse(os.path.join('accounts', 'sign_in.html'), context={'request': request})


@login_router.post("/", response_class=RedirectResponse)
async def login(
    db : Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()) -> RedirectResponse:

    to_login_user = UserCreate(user_id=form_data.username, password=form_data.password)
    if not authenticate_user(db, to_login_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": to_login_user.user_id}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="http://118.67.131.88:30001/")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="token_type", value="bearer", httponly=True)
    response.status_code = 302
    return response
    return {"access_token": access_token, "token_type": "bearer"}
    # spec에 따르면 위 예제처럼 access_token과 token_type을 반드시 리턴해주어야 한다고 함.