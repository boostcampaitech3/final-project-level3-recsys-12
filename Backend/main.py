import os

from utils import templates

from fastapi import FastAPI,  Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from router.login import login_router
from router.register import register_router
from router.mypage import mypage_router


app = FastAPI()
app.mount(
    "/templates",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'templates')),
    name="templates",
)

app.include_router(login_router)
app.include_router(register_router)
app.include_router(mypage_router)

@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html" , context={"request": request})