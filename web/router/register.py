import os
from fastapi import APIRouter, Form, Request, Depends
from db.schemas import UserCreate, User
from db.crud import create_user, get_user
from utils import templates, get_db

from sqlalchemy.orm import Session

register_router = APIRouter(prefix="/register")


@register_router.post("/")
async def register(
    request: Request,
    db: Session = Depends(get_db),
    user_id: str=Form(...), 
    password: str=Form(...),
    name: str=Form(...),
    ):
    if get_user(db, user_id) is None:
        user_create = UserCreate(
            id=user_id, 
            password=password)
        
        user_info = User(
            id=user_id,
            name=name
            )

        create_user(db, user_create, user_info)
        context = {
            'request': request,
            'success_mesage': '회원가입에 성공하셨습니다.',
            'login_required': True
        }
        return templates.TemplateResponse(os.path.join('user', 'account_success.html'), context=context)
    else:
        context = {
            'request': request,
            'fail_message': '회원가입에 실패 하셨습니다.',
            'login_required': True
        }
        return templates.TemplateResponse(os.path.join('user', 'account_fail.html'), context=context)



