from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='./templates/accounts')

login_router = APIRouter(prefix="/login")
register_router = APIRouter(prefix="/register")


@register_router.get("/")
def get_register_form(request: Request):
    return templates.TemplateResponse('register_form.html', context={'request': request})


@register_router.post("/")
def register():
    return {"message": "회원가입 성공"}


@login_router.get("/")
def get_login_form(request: Request):
    return templates.TemplateResponse('login_form.html', context={'request': request})


@login_router.post("/")
def login(username: str=Form(...), password: str=Form(...)):
    return {"username": username, "password": password}