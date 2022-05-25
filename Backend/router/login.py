import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 상위 경로(Backend)를 절대 결로에 추가

from fastapi import APIRouter, Form, Request, Depends
from utils import templates, get_db
from db.crud import verification_user
from db.schemas import UserCreate

from sqlalchemy.orm import Session

login_router = APIRouter(prefix="/login")

@login_router.get("/")
def get_login_form(request: Request):
    return templates.TemplateResponse(os.path.join('accounts', 'login_form.html'), context={'request': request})


@login_router.post("/")
def login(
    db: Session = Depends(get_db),
    user_id: str=Form(...), 
    password: str=Form(...)):

    try_user = UserCreate(
        user_id=user_id,
        password=password
    )

    if verification_user(db, try_user) is True:
        return {"message": '로그인 성공'}
    else:
        return {"message": '로그인 실패'}