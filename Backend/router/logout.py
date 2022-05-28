from fastapi import APIRouter, Request, Response
from db.models import User
from utils import templates

logout_router = APIRouter(prefix='/logout')

@logout_router.get("/")
def get_login_form(request: Request):
    response = templates.TemplateResponse("main_logout.html", {"request": request})
    response.delete_cookie("access_token")
    response.delete_cookie("token_type")
    return response
