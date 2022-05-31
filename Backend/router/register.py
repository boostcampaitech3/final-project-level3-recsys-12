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
        return templates.TemplateResponse(os.path.join('sign_up', 'success.html'), context={'request': request})
    else:
        return templates.TemplateResponse(os.path.join('sign_up', 'fail.html'), context={'request': request})



