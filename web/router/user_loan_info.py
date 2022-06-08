import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from utils import get_db, get_current_user, templates
from db.crud import get_loan_of_user
from db import models

from sqlalchemy.orm import Session

loan_info = APIRouter(prefix="/loan_info")


# resource를 식별해야하므로 path parameter가 더 적합
@loan_info.get("/", response_class=JSONResponse)
def user_loan_info(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    context = {'request': request}
    if current_user is False:
        context['login_required'] = True
        context['fail_message'] = '로그인이 필요합니다.'
        return templates.TemplateResponse(os.path.join('user', 'account_fail.html'), context=context)
    else:
        loan_books = get_loan_of_user(db, current_user.id)
        list_loaned_books = list()
        list_returned_books = list()
        for loan_book in loan_books:
            dict_info = dict()
            dict_info['loan_at'] = str(loan_book.loan_at)
            dict_info['isbn'] = loan_book.book_id
            dict_info['title'] = loan_book.book.title
            dict_info['img_URL'] = loan_book.book.image_URL
            dict_info['is_return'] = loan_book.is_return
            if dict_info['is_return'] is True:
                dict_info['due'] = False
                dict_info['return_at'] = str(loan_book.return_at)
                list_returned_books.append(dict_info)
            else:
                dict_info['due'] = str(loan_book.due)
                list_loaned_books.append(dict_info)

        sorted_loaned_books = sorted(list_loaned_books, key=lambda book_info: book_info['loan_at'])
        sorted_retured_books = sorted(list_returned_books, key=lambda book_info: book_info['return_at'], reverse=True)

        context['login_required'] = False
        context['loaned_info'] = sorted_loaned_books
        context['returned_info'] = sorted_retured_books
        context['all_loan_length'] = len(list_loaned_books) + len(list_returned_books)
        
        response = templates.TemplateResponse(os.path.join('user', 'loan_history.html'), context=context)
        response.set_cookie(key="previous_url", value="http://118.67.131.88:30001/loan_info/", httponly=True)
        return response