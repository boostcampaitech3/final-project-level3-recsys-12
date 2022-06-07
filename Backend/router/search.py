from typing import List
from fastapi import APIRouter, Form, Request, Depends, HTTPException

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from utils import templates, get_db


from db import crud, schemas

search_router = APIRouter(prefix="/search")


@search_router.get("/title/", response_class=HTMLResponse)
def search(request: Request, db: Session = Depends(get_db), text: str = ""):
    search= crud.search_by_title(db, search_text=text)
    context = {
        "request": request,
        "text": text,
        "search": search,
    }

    return templates.TemplateResponse(os.path.join("book", "search_item.html"), context)


@search_router.get("/author/", response_class=HTMLResponse)
def search(request: Request, db: Session = Depends(get_db), text: str = ""):
    search= crud.search_by_author(db, search_text=text)
    context = {
        "request": request,
        "text": text,
        "search": search,
    }

    return templates.TemplateResponse(os.path.join("book", "search_author.html"), context)
