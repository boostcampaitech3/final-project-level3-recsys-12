from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from db.models import User
from utils import templates

logout_router = APIRouter(prefix='/logout')

@logout_router.get("/")
def logout() -> RedirectResponse:
    response = RedirectResponse(url="http://118.67.131.88:30001/")
    response.delete_cookie("access_token")
    response.delete_cookie("token_type")
    response.status_code = 302
    return response
