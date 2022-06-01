from fastapi import APIRouter, Form, Request, Depends, HTTPException

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from utils import templates, get_db

from router.loan_func import loan_router, return_router
from db import crud

book_router = APIRouter(prefix="/books")
book_router.include_router(loan_router)
book_router.include_router(return_router)

@book_router.get("/{id}", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(get_db), id: str = ""):
    book = crud.get_item(db, item_id=id) 
    genres = crud.all_genres(db) 
    context = {
        "request": request,
        "genres": genres,
        "book": book,
    }
    return templates.TemplateResponse("detail.html", context)