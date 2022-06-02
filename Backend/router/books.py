from typing import List
from fastapi import APIRouter, Form, Request, Depends, HTTPException

from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from utils import templates, get_db, get_current_user

from router.loan_func import loan_router, return_router

from db import crud, schemas, models

book_router = APIRouter(prefix="/books")


@book_router.get("/", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    books = crud.all_items(db, skip=0, limit=12)
    if current_user is False:
        login_required = True
        username = None
    else:
        login_required = False
        username = current_user.name

    context = {
        "request": request,
        "books": books,  
        "login_required": login_required,
        "username": username
        }
    return templates.TemplateResponse("html/shop/v3.html", context)



@book_router.get("/{book_id}", response_class=HTMLResponse)
def read_item(request: Request, db: Session = Depends(get_db), book_id: str= "", current_user: models.User = Depends(get_current_user)):
    book = crud.get_item(db, item_id=book_id)
    book_authors = crud.get_authors_by_item(db, item_id=book_id)[0].author_id
    author = crud.get_item_by_author(db, author_id=book_authors)

    if current_user:
        loan_status = False if crud.get_loan_info(db, current_user.id, book_id) else True
        if crud.get_user_item_rating(db, current_user.id, book_id):
            rating = crud.get_user_item_rating(db, current_user.id, book_id).rating
        else:
            rating = 0
        context = {
        "request": request,
        "book": book,
        "book_authors": book_authors,
        "author": author,
        "login_required": False,
        "loan_status": loan_status,
        "rating": rating
        }
        return templates.TemplateResponse("html/shop/single-product-v1.html", context)
    else:
        context = {
        "request": request,
        "book": book,
        "book_authors": book_authors,
        "author": author,
        "login_required": True,
        }
        return templates.TemplateResponse("html/shop/single-product-v1.html", context)


@book_router.post("/{book_id}/rating", response_class=RedirectResponse)
async def rating(
    db: Session = Depends(get_db), 
    book_id: str= "", 
    current_user: models.User = Depends(get_current_user),
    rating: int = Form(...)
    ) -> RedirectResponse:

    crud.create_user_item_rating(db, user=current_user.id, item=book_id, rating=rating)
    response = RedirectResponse(url="http://127.0.0.1:8000/books/{book_id}")
    return response


@book_router.put("/{book_id}/rating", response_class=RedirectResponse)
async def modify_rating(
    db: Session = Depends(get_db), 
    book_id: str= "", 
    current_user: models.User = Depends(get_current_user),
    rating: int = Form(...)
    ) -> RedirectResponse:

    crud.modify_user_item_rating(db, user=current_user.id, item=book_id, rating=rating)
    response = RedirectResponse(url="http://127.0.0.1:8000/books/{book_id}")
    return response


@book_router.get("/{book_id}/loan")
def loan_book_func(book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    crud.create_book_loan(db, current_user.id, book_id)
    response = RedirectResponse(url="http://127.0.0.1:8000/books/{book_id}")
    return response

@book_router.get("/{book_id}/return")
def return_book_func(book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    crud.return_book(db, current_user.id, book_id)
    response = RedirectResponse(url="http://127.0.0.1:8000/books/{book_id}")
    return response

@book_router.get("/loan")
def return_book_func(book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    crud.return_book(db, current_user.id, book_id)
    response = RedirectResponse(url="http://127.0.0.1:8000/books/{book_id}")
    return response
