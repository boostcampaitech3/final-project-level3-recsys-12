import os, yaml
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import desc
from sqlalchemy import and_
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

def get_current_time() -> datetime:
    return datetime.now(timezone(timedelta(hours=9)))


def create_book_loan(db: Session, user_id: str, book_id: str):
    days_of_loan_term = 7
    loan_at = get_current_time()
    loan_info = schemas.Loan(
        book_id=book_id,
        user_id=user_id,
        loan_at = loan_at,
        due = loan_at + timedelta(days=days_of_loan_term),
        count = 0,
        is_return = False
    )

    db_loan = models.Loan(
        **loan_info.dict(),
        )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    return db_loan


def get_loan_info(db: Session, user_id: str, book_id: str):
    loan_info = db.query(models.Loan).filter(
        and_(
            models.Loan.user_id==user_id, 
            models.Loan.book_id==book_id,
            models.Loan.is_return==False
            )).first()
    
    return loan_info


def create_user_item_rating(db: Session, user_id: str, book_id: str, rating: int):
    rating_info = schemas.Rating(
        user=user_id,
        item=book_id,
        rating=rating
    )
    db_rating = models.Rating(
        **rating_info.dict()
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating

def get_user_item_rating(db: Session, user_id: str, book_id: str):
    rating_info = db.query(models.Rating).filter(
        and_(
            models.Rating.user == user_id,
            models.Rating.item == book_id
        )).first()
    return rating_info


def modify_user_item_rating(db: Session, user_id: str, book_id: str, rating: int):
    rating_info = get_user_item_rating(db, user_id=user_id, book_id=book_id)
    rating_info.rating = rating
    db.commit()
    return rating_info
    


def return_book(db: Session, user_id: str, book_id: str):
    loan_info = get_loan_info(db, user_id=user_id, book_id=book_id)
    loan_info.is_return = True
    loan_info.return_at = get_current_time()

    db.commit()


def get_loan_of_user(db: Session, user_id: str):
    return db.query(models.Loan).filter(user_id==user_id).all()