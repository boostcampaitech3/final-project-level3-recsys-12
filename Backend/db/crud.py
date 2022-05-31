import os, yaml
from sqlalchemy.orm import Session
from . import models, schemas

from passlib.context import CryptContext


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config_hash.yaml')
with open(CONFIG_PATH) as config:
    conf = yaml.load(config, Loader=yaml.FullLoader)
    SECRET_KEY = conf['secret_key']
    ALGORITHM = conf['ALGORITHM']
    SCHEMES = conf['SCHEMES']

pwd_context = CryptContext(schemes=[SCHEMES], deprecated="auto")


def get_user(db: Session, id: str):
    return db.query(models.User).filter(models.User.id==id).first()


def create_user(db: Session, user: schemas.UserCreate, user_info: schemas.User):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        hashed_password=hashed_password,
        **user_info.dict(),
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def all_genres(db:Session):
    return db.query(models.Genre).all()


# 최신 책 찾기
def get_recent_item(db: Session, skip: int = 0, limit: int = 2):
    return db.query(models.Book).order_by(desc(models.Book.publication_year)).offset(skip).limit(limit).all()

# ID로 책 찾기
def get_item(db:Session, item_id: str):
    return db.query(models.Book).filter(models.Book.id == item_id).first()

# 제목으로 책 찾기
def get_items_by_title(db:Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


# 해당 연도 책 찾기
def get_items_on_year(db:Session, year: int):
    return db.query(models.Book).filter(models.Book.publication_year == year).first()


# 각 장르별 책 정보 모음
def get_items_by_genre(db:Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first().books

# 각 저자별 책 정보 모음
def get_items_by_author(db:Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first().books


# 책 제목으로 검색하기
def search_by_title(db:Session, search_text: str):
    search = "%{}%".format(search_text)
    return db.query(models.Book).filter(models.Book.title.like(search)).all()

# 책 내용으로 검색하기
def search_by_description(db:Session, search_text: str):
    search = "%{}%".format(search_text)
    return db.query(models.Book).filter(models.Book.description.like(search)).all()

# 저자로 검색하기
def search_by_author(db:Session, search_text: str):
    search = "%{}%".format(search_text)
    return db.query(models.Author).filter(models.Author.name.like(search)).all()
