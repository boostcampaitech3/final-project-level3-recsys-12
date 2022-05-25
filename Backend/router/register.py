import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 상위 경로(Backend)를 절대 결로에 추가

from fastapi import APIRouter, Form, Request, Depends
from db.schemas import UserCreate, User
from db.crud import create_user
from utils import templates, get_db

from sqlalchemy.orm import Session

register_router = APIRouter(prefix="/register")

@register_router.get("/")
def get_register_form(request: Request):
    return templates.TemplateResponse(os.path.join('accounts', 'register_form.html'), context={'request': request})


@register_router.post("/")
def register(
    db: Session = Depends(get_db),
    user_id: str=Form(...), 
    password: str=Form(...),
    name: str=Form(...),
    age: int=Form(...),
    city: str=Form(...),
    state: str=Form(...),
    country: str=Form(...),
    ):
    user_create = UserCreate(
        user_id=user_id, 
        password=password)
    user_info = User(
        user_id=user_id,
        name=name,
        age=age,
        city=city,
        state=state,
        country=country
        )
    create_user(db, user_create, user_info)

    return {"message": "회원가입 성공"}



