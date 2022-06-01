import os

from utils import templates, get_db, get_current_user
from db.models import User
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI,  Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from router.login import login_router
from router.register import register_router
from router.mypage import mypage_router
from router.logout import logout_router
from router.recsys import send_to_unreal
from router.books import book_router
from router.genres import genre_router
from router.user_loan_info import loan_info

app = FastAPI()
routers = [login_router, register_router, mypage_router, logout_router, send_to_unreal, book_router, genre_router, loan_info]
for router in routers:
    app.include_router(router)

app.mount(
    "/templates",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'templates')),
    name="templates",
)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, db: Session = Depends(get_db)):
    
    token: str = request.cookies.get("access_token")
    if token is not None:
        # token이 있을 때
        current_user = await get_current_user(request=request, db=db)
        login_required = False
        username = current_user.name
    else:
        # token이 없을 때
        login_required = True
        username = None

    context = {
        "request": request,
        "login_required": login_required,
        "username": username
    }
    return templates.TemplateResponse("html/home/index.html" , context)