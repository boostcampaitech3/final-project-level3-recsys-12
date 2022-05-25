from utils import templates

from fastapi import FastAPI,  Request
from fastapi.responses import HTMLResponse

from router.login import login_router
from router.register import register_router


app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)


@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html" , context={"request": request})