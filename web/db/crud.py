from itertools import groupby
from operator import ge
from typing import List
import os, yaml
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func, distinct
from . import models, schemas
from collections import Counter
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
    return db_user



def all_genres(db:Session):
    return db.query(models.Genre).all()

# def all_items(db:Session):
#     return db.query(models.Book).all()

def all_items(db:Session, skip: int = 0, limit: int = 12):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_genre(db:Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()

def get_author(db:Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_genres(db:Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first().books

# 최신 책 찾기
def get_recent_item(db: Session, skip: int = 0, limit: int = 7):
    return db.query(models.Book).order_by(desc(models.Book.publication_year)).offset(skip).limit(limit).all()

# ID로 책 찾기
def get_item(db:Session, item_id: str):
    return db.query(models.Book).filter(models.Book.id == item_id).first()

# 제목으로 책 찾기
def get_items_by_title(db:Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()

# 아이템의 저자 찾기
def get_authors_by_item(db:Session, item_id: str):
    book_info = db.query(models.Book).filter(models.Book.id == item_id).first()
    if book_info:
        return book_info.authors
    else:
        return None

# 저자 정보로 책 찾기
def get_item_by_author(db:Session, author_id: str):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


# 해당 연도 책 찾기
def get_items_on_year(db:Session, year: int):
    return db.query(models.Book).filter(models.Book.publication_year == year).first()


# 각 장르별 책 정보 모음
def get_items_by_genre(db:Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first().books

# 해당 저자가 쓴 책 정보 모음
def get_items_by_author(db:Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first().books


# 책 제목으로 검색하기
def search_by_title(db:Session, search_text: str):
    search = "%{}%".format(search_text)
    return db.query(models.Book).filter(models.Book.title.like(search)).all()

# 책 내용으로 검색하기
def search_by_description(db:Session, search_text: str):
    search = "%{}%".format(search_text)
    return db.query(models.Book).filter(models.Book.synopsis.like(search)).all()

# 저자로 검색하기
def search_by_author(db:Session, search_text: str):
    search = "%{}%".format(search_text)
    return db.query(models.Author).filter(models.Author.name.like(search)).all()

# 인기있는 카테고리
def popular_genre(db:Session):
    book_genre = db.query(models.BookGenre.genre_id).all()
    count = Counter(book_genre).most_common(5)
    response = list()
    for i in count:
        idx = 0
        genre = get_genre(db, genre_id=i[0][0])
        books = get_items_by_genre(db, genre_id=genre.id)
        book_info = dict()
        book_list = list()
        for book in books:
            if idx == 12:
                break
            book_list.append(book.book)
            idx += 1
        book_info["genre_id"] = genre.id
        book_info["genre_name"] = genre.name
        book_info["books"] = book_list
        response.append(book_info)
    return response

def popular_author(db:Session):
    book_author = db.query(models.BookAuthor.author_id).all()
    count = Counter(book_author).most_common(5)
    response = list()
    for i in count:
        idx = 0
        author = get_author(db, author_id=i[0][0])
        books = get_items_by_author(db, author_id=author.id)
        book_info = dict()
        book_list = list()
        for book in books:
            if idx == 12:
                break
            book_list.append(book.book)
            idx += 1
        book_info["author_id"] = author.id
        book_info["author_name"] = author.name
        book_info["books"] = book_list
        response.append(book_info)
    return response


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


def current_time() -> datetime:
    # 현재 시간을 가져온다. 한국은 utc기준으로 +9 hour이다.
    return datetime.utcnow() + timedelta(hours=9)

def create_book_loan(db: Session, user_id: str, book_id: str):
    # 유저가 책을 빌리면 대출 관련 데이터를 생성한다.
    days_of_loan_term = 7
    loan_at = current_time()
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
    # user와 book에 대해 대출 정보를 가져온다. : 언제 대출 했는지, 언제 반납하는지 등.
    loan_info = db.query(models.Loan).filter(
        and_(
            models.Loan.user_id==user_id, 
            models.Loan.book_id==book_id,
            models.Loan.is_return==False
            )).first()
    
    return loan_info 


def return_book(db: Session, user_id: str, book_id: str):
    # 책 반납하는 기능: is_return을 true로하고, return 시간 기록
    loan_info = get_loan_info(db, user_id, book_id)
    loan_info.is_return = True
    loan_info.return_at = current_time()

    db.commit()
    return loan_info


def get_loan_of_user(db: Session, user_id: str):
    # user의 대출 이력을 가져온다.
    return db.query(models.Loan).filter(models.Loan.user_id==user_id).all()


def get_inference_of_user(db: Session, user_id: str):
    return db.query(models.Inference).filter(models.Inference.user==user_id).all()

