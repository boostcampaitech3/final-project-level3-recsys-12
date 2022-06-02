from typing import List
from fastapi import APIRouter, Form, Request, Depends, HTTPException

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from utils import templates, get_db


from db import crud, schemas

search_router = APIRouter(prefix="/search")


@search_router.get("/", response_model=List[schemas.BookBase])
def search(db: Session = Depends(get_db), text: str = ""):
    search= crud.search_by_title(db, search_text=text)
    return search


