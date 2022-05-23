from typing import List

from fastapi import FastAPI,  Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse

from fastapi.templating import Jinja2Templates

from router.accounts import login_router, register_router

# models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='./templates')

app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)


@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html" , context={"request": request})