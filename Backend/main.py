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

from utils import get_current_user

app = FastAPI()
app.mount(
    "/templates",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'templates')),
    name="templates",
)

app.include_router(login_router)
app.include_router(register_router)
app.include_router(mypage_router)
app.include_router(logout_router)
app.include_router(send_to_unreal)

@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    token: str = request.cookies.get("access_token")
    if token is not None:
        return templates.TemplateResponse("main_login.html" , context={"request": request})
    else:
        return templates.TemplateResponse("main_logout.html" , context={"request": request})