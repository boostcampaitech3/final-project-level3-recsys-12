import os

from fastapi import APIRouter, Form, Request, Depends

from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from utils import templates, get_db, get_current_user

from db import crud, models

book_router = APIRouter(prefix="/books")


@book_router.get("/", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    books = crud.all_items(db, skip=0, limit=12)
    popular_genre = crud.popular_genre(db)
    popular_author = crud.popular_author(db)
    if current_user is False:
        login_required = True
        username = None
        context = {
            "request": request,
            "books": books,  
            "login_required": login_required,
            "username": username,
            "popular_genre": popular_genre,
            "popular_author": popular_author,
        }
    else:
        login_required = False
        username = current_user.name
        recommendation_items = crud.get_inference_of_user(db, user_id=current_user.id)
        rec_books = list()
        for item in recommendation_items:
            rec_books.append(item.item_info)
        context = {
            "request": request,
            "books": books,  
            "login_required": login_required,
            "username": username,
            "popular_genre": popular_genre,
            "popular_author": popular_author,
            "rec_books": rec_books,
        }

    return templates.TemplateResponse(os.path.join('book', 'data.html'), context)


@book_router.get("/populargenre/{genre_id}", response_class=HTMLResponse)
def read_genre(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), genre_id: int = 0):
    books = crud.all_items(db, skip=0, limit=12)
    popular_genre = crud.popular_genre(db)
    popular_author = crud.popular_author(db)
    book_res = list()
    for genre in popular_genre:
        if genre['genre_id'] == genre_id:
            for book in genre['books']:
                book_res.append(book)

    if current_user is False:
        login_required = True
        username = None
        context = {
            "request": request,
            "books": books,  
            "login_required": login_required,
            "username": username,
            "popular_genre": popular_genre,
            "popular_author": popular_author,
            "book_res": book_res,
        }
    else:
        login_required = False
        username = current_user.name
        recommendation_items = crud.get_inference_of_user(db, user_id=current_user.id)
        rec_books = list()
        for item in recommendation_items:
            rec_books.append(item.item_info)
        context = {
            "request": request,
            "books": books,  
            "login_required": login_required,
            "username": username,
            "popular_genre": popular_genre,
            "popular_author": popular_author,
            "book_res": book_res,
            "rec_books": rec_books,
        }

    
    return templates.TemplateResponse(os.path.join('book', 'genre.html'), context)


@book_router.get("/popularauthor/{author_id}", response_class=HTMLResponse)
def read_genre(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), author_id: int = 0):
    books = crud.all_items(db, skip=0, limit=12)
    popular_genre = crud.popular_genre(db)
    popular_author = crud.popular_author(db)
    book_res = list()
    for author in popular_author:
        if author['author_id'] == author_id:
            for book in author['books']:
                book_res.append(book)

    if current_user is False:
        login_required = True
        username = None
        context = {
            "request": request,
            "books": books,  
            "login_required": login_required,
            "username": username,
            "popular_genre": popular_genre,
            "popular_author": popular_author,
            "book_res": book_res,
        }
    else:
        login_required = False
        username = current_user.name
        recommendation_items = crud.get_inference_of_user(db, user_id=current_user.id)
        rec_books = list()
        for item in recommendation_items:
            rec_books.append(item.item_info)
        context = {
            "request": request,
            "books": books,  
            "login_required": login_required,
            "username": username,
            "popular_genre": popular_genre,
            "popular_author": popular_author,
            "book_res": book_res,
            "rec_books": rec_books,
        }

    return templates.TemplateResponse(os.path.join('book', 'author.html'), context)



@book_router.get("/{book_id}", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db), book_id: str= "", current_user: models.User = Depends(get_current_user)):
    book = crud.get_item(db, item_id=book_id)
    if crud.get_authors_by_item(db, item_id=book_id):
        book_authors = crud.get_authors_by_item(db, item_id=book_id)[0].author_id
        author = crud.get_item_by_author(db, author_id=book_authors)
    else:
        book_authors = ""
        author = ""

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
        "user": current_user,
        "login_required": False,
        "loan_status": loan_status,
        "rating": rating
        }
        return templates.TemplateResponse(os.path.join('book', 'detail.html'), context)
    else:
        loan_status = True
        context = {
        "request": request,
        "book": book,
        "book_authors": book_authors,
        "author": author,
        "login_required": True,
        "loan_status": loan_status,
        "rating": 0,
        }
        return templates.TemplateResponse(os.path.join('book', 'detail.html'), context)


@book_router.post("/{book_id}/ratingcreate", response_class=RedirectResponse)
async def rating(
    request: Request,
    db: Session = Depends(get_db), 
    book_id: str= "", 
    current_user: models.User = Depends(get_current_user),
    rating: int = Form(...)
    ) -> RedirectResponse:

    context = {'request': request}
    if current_user is False:
        context['login_required'] = True
        context['fail_message'] = '로그인이 필요합니다.'
        return templates.TemplateResponse(os.path.join("user", "account_fail.html"), context)
    else:          
        crud.create_user_item_rating(db, user_id=current_user.id, book_id=book_id, rating=rating)
        response = RedirectResponse(url=f"http://118.67.131.88:30001/books/{book_id}")
        response.status_code = 302
        return response


@book_router.post("/{book_id}/ratingmodify", response_class=RedirectResponse)
async def modify_rating(
    db: Session = Depends(get_db), 
    book_id: str= "", 
    current_user: models.User = Depends(get_current_user),
    rating: int = Form(...)
    ) -> RedirectResponse:

    crud.modify_user_item_rating(db, user_id=current_user.id, book_id=book_id, rating=rating)
    response = RedirectResponse(url=f"http://118.67.131.88:30001/books/{book_id}")
    response.status_code = 302
    return response


@book_router.get("/{book_id}/loan")
def loan_book_func(request: Request, book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    context = {'request': request}
    if current_user is False:
        context['login_required'] = True
        context['fail_message'] = '로그인이 필요합니다.'
        return templates.TemplateResponse(os.path.join("user", "account_fail.html"), context)
    else:          
        crud.create_book_loan(db, current_user.id, book_id)
        response = RedirectResponse(url=f"http://118.67.131.88:30001/books/{book_id}")
        response.status_code = 302
        return response


# redirect 주소 수정
@book_router.get("/{book_id}/return")
def return_book_func(book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    crud.return_book(db, current_user.id, book_id)
    response = RedirectResponse(url=f"http://118.67.131.88:30001/books/{book_id}")
    response.status_code = 302
    return response