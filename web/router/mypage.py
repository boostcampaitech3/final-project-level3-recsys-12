from fastapi import APIRouter, Depends
from utils import templates, get_current_user
from db import models, schemas

mypage_router = APIRouter(prefix="/mypage")    

@mypage_router.get("/")
async def read_users_(current_user: models.User = Depends(get_current_user)):
    return schemas.User(**(current_user.__dict__))