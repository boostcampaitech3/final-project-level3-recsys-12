# basic
from datetime import datetime, timedelta
import os

# fastapi
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse

# token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

# defined objects
from utils import get_db, templates
from db.crud import get_user
from db.crud import pwd_context, SECRET_KEY, ALGORITHM
from db.schemas import UserCreate

# type hint
from sqlalchemy.orm import Session
from typing import Optional

ACCESS_TOKEN_EXPIRE_MINUTES = 360

login_router = APIRouter(prefix="/login")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# tokenURL: user가 token을 얻기 위해 id와 password를 send하는 곳.
#         : 상대적인 경로이다. ./login


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, to_login_user: UserCreate) -> bool:
    user = get_user(db, to_login_user.id)
    if user is None:
        # 존재하지 않는 유저가 로그인 시도
        return False
    if not verify_password(to_login_user.password, user.hashed_password):
        # 유저가 존재는 하지만 비밀번호가 틀림
        return False
    return True


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta: expire = datetime.utcnow() + expires_delta
    else: expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def make_access_token( db: Session, user: UserCreate):
    if authenticate_user(db, user) is False:
        # 로그인 실패: 존재하지 않는 유저 또는 비밀번호 틀림
        return False
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return access_token


# unreal engine에서 login을 확인할 때
@login_router.get("/")
def get_login_form(user_id: str = None, password: str = None, db: Session = Depends(get_db)):
    token_value = False
    error_message = None
    if user_id:
        try:
            to_login_user = UserCreate(id=user_id, password=password)
            token_value = make_access_token(db, to_login_user)
        except Exception as e:
            token_value = False
            error_message = e
    if token_value is False:
        if error_message is None:
            ret_json = {"access_toekn": "로그인에 실패하셨습니다."}
        else:
            ret_json = {"access_token": error_message}
    ret_json = {"access_token": token_value}
    return JSONResponse(content=ret_json)


@login_router.post("/")
async def login(
    request: Request,
    db : Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()) -> RedirectResponse:

    try:
        to_login_user = UserCreate(id=form_data.username, password=form_data.password)
        access_token = make_access_token(db, to_login_user)
    except:
        # 이메일 형식이 맞지 않음.
        access_token = False
    finally:
        if access_token is False:
            # 로그인 실패 했을 경우: 존재하지 않는 이메일, 틀린 비밀번호, 토큰 만료 등
            context = {
                'request': request,
                'fail_message': '로그인에 실패 하셨습니다.',
                'login_required': True,
            }
            return templates.TemplateResponse(os.path.join('user', 'account_fail.html'), context=context)
        else:
            response = RedirectResponse(url="http://118.67.131.88:30001/")
            response.set_cookie(key="access_token", value=access_token, httponly=True)
            response.set_cookie(key="token_type", value="bearer", httponly=True)
            # spec에 따르면 위 예제처럼 access_token과 token_type을 반드시 리턴해주어야 한다고 함.
            response.status_code = 302
            return response
