from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from db.crud import get_user_recsys_list
from utils import get_db

send_to_unreal = APIRouter(prefix="/rec")

fake_db = {
    'rec1': {
        'title': 'test1',
        'url': 'https://pictures.abebooks.com/isbn/9780000092878-us-300.jpg'
    },
    'rec2': {
        'title': 'test2',
        'url': 'https://pictures.abebooks.com/isbn/9780000477156-us-300.jpg'

    },
    'rec3': {
        'title': 'test3',
        'url': 'https://pictures.abebooks.com/isbn/9780000004543-us-300.jpg'
    }
}

# 정렬, 필터링을 하는 것이므로 Query Parameter가 더 적합
@send_to_unreal.get("/{user_id}")
async def get_rec_result(user_id: str, db=Depends(get_db)):
    # A19S4FX6C54TNV@gmail.com
    recsys_results = get_user_recsys_list(db, user_id)
    dict_recsys_results = dict()
    for idx, recsys_result in enumerate(recsys_results):
        print(recsys_result.item)
        dict_info = dict()
        dict_info['title'] = recsys_result.rec_item.title
        dict_info['url'] = recsys_result.rec_item.image_URL

        dict_recsys_results[f'rec{idx}'] = dict_info
    
    print(dict_recsys_results)
    return JSONResponse(content=fake_db)
