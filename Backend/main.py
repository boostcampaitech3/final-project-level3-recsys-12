import os
from re import template

from utils import templates

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

from utils import get_current_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.include_router(login_router)
app.include_router(register_router)
app.include_router(mypage_router)
app.include_router(logout_router)
app.include_router(send_to_unreal)
app.include_router(book_router)
app.include_router(genre_router)

@app.get("/", response_class=HTMLResponse)
def main(request: Request, db: Session = Depends(get_db)):
    
    token: str = request.cookies.get("access_token")
    if token is not None:
        status = False
    else:
        status = True
    context = {
        "request": request,
        "status": status,
    }
    return templates.TemplateResponse("html/home/index.html" , context)