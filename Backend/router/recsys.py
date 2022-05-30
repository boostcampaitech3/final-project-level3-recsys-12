from fastapi import APIRouter
from fastapi.responses import JSONResponse

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
@send_to_unreal.get("/")
def get_rec_result(user_id):
    print(user_id)
    return JSONResponse(content=fake_db)
