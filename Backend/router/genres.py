from fastapi import APIRouter, Form, Request, Depends, HTTPException

from fastapi.responses import HTMLResponse
from numpy import tensordot
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from utils import templates, get_db
from typing import List


from db import crud, schemas

genre_router = APIRouter(prefix="/genres")


# @genre_router.get("/{id}", response_class=HTMLResponse)
# def read_item(request: Request, db: Session = Depends(get_db), id: int = 1):
#     genres = crud.get_item_by_genre(db, genre_id=id)  
#     return templates.TemplateResponse("collect.html", {"request": request, "genres": genres})


@genre_router.get("/{id}", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(get_db), id: int = 1):
    genre_books = crud.get_genres(db, genre_id=id)
    genres = crud.all_genres(db)
    context = {
        "request": request,
        "genre_books": genre_books,
        "genres": genres,
    }
    return templates.TemplateResponse("collect.html", context)

