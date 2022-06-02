from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db.crud import get_inference_of_user
from utils import get_db

send_to_unreal = APIRouter(prefix="/rec")


# 정렬, 필터링을 하는 것이므로 Query Parameter가 더 적합
@send_to_unreal.get("/{user_id}")
async def get_rec_result(request: Request, user_id: str, db: Session = Depends(get_db)):
    # A0496269KM4VQ5JO5KRY@gmail.com
    # AZVXGCT3CHIS5@gmail.com
    inference_books = get_inference_of_user(db, user_id)
    inference_dict = dict()

    for idx, inference_book in enumerate(inference_books):
        book_info = dict()
        book_info['isbn'] = inference_book.item_info.id
        book_info['title'] = inference_book.item_info.title
        book_info['url'] = inference_book.item_info.image_URL

        inference_dict[f'rec{idx+1}'] = book_info
    
    print(inference_dict)

    return JSONResponse(content=inference_dict)