from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from utils import get_db, get_current_user
from db.crud import create_book_loan, return_book
from db import models

from sqlalchemy.orm import Session

loan_router = APIRouter(prefix="/loan")
return_router = APIRouter(prefix="/return")

# resource를 식별해야하므로 path parameter가 더 적합
@loan_router.get("/{book_id}")
def loan_book_func(book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    create_book_loan(db, current_user.id, book_id)
    response = RedirectResponse(url="http://118.67.131.88:30001/")
    return response


# resource를 식별해야하므로 path parameter가 더 적합
@return_router.get("/{book_id}")
def return_book_func(book_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    return_book(db, current_user.id, book_id)
    response = RedirectResponse(url="http://118.67.131.88:30001/")
    return response