from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import Json

from utils import get_db, get_current_user
from db.crud import get_loan_of_user
from db import models

from sqlalchemy.orm import Session

loan_info = APIRouter(prefix="/loan_info")

# resource를 식별해야하므로 path parameter가 더 적합
@loan_info.get("/", response_class=JSONResponse)
def user_loan_info(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan_books = get_loan_of_user(db, current_user.id)
    dict_loan_books = dict()
    for idx, loan_book in enumerate(loan_books):
        dict_info = dict()
        dict_info['isbn'] = loan_book.book_id
        dict_info['title'] = loan_book.book.title
        dict_info['publication_year'] = loan_book.book.publication_year
        dict_info['is_return'] = loan_book.is_return

        dict_loan_books[idx] = dict_info
    return dict_loan_books