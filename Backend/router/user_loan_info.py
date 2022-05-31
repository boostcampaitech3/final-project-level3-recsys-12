from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from utils import get_db, get_current_user
from db.crud import return_book
from db import models

from sqlalchemy.orm import Session

loan_info = APIRouter(prefix="/loan_info")

# resource를 식별해야하므로 path parameter가 더 적합
@loan_info.get("/{book_id}")
def user_loan_info(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # book_id = '0001844423'
    return_book(db, current_user.id, book_id)
    response = RedirectResponse(url="http://118.67.131.88:30001/")
    return response