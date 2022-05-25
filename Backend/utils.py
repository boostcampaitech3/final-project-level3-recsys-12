import os
from db.database import SessionLocal
from fastapi.templating import Jinja2Templates

base_dir = os.path.abspath(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, 'templates'))

# Dependency
# 오류가 나도 session은 닫자!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()