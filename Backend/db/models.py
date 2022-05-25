from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text

from . import database

class User(database.Base):
    __tablename__ = "user_info"

    user_id = Column(String, primary_key=True, index=True)
    # index는 query performance를 좋게 하기 위해 사용한다.
    hashed_password = Column(String, nullable=False)
    age = Column(Integer)
    name = Column(String)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    # 장르 선호도
    # created_at = Column(DateTime(timezone=True), server_default=func.now())


class Book(database.Base):
    __tablename__ = "book_info"

    isbn = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    publication_year = Column(Integer)
    image_S_URL = Column(String)
    image_M_URL = Column(String)
    image_L_URL = Column(String)


class Rating(database.Base):
    __tablename__ = "ratings"
    user_id = Column(String, ForeignKey('user_info.user_id'), primary_key=True)
    isbn = Column(String, ForeignKey('book_info.isbn'), primary_key=True)
    rating = Column(Integer)


class UserQnA(database.Base):
    __tablename__ = 'user_qna'

    board_id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('user_info.user_id'))
    content = Column(Text)
    create_date = Column(DateTime)
    is_answered = Column(Boolean)


class Loan(database.Base):
    __tablename__ = 'loan_info'
    isbn = Column(String,  ForeignKey('book_info.isbn'), primary_key=True)
    user_id = Column(String, ForeignKey('user_info.user_id'), primary_key=True)
    due = Column(DateTime)
    count = Column(Integer)


if __name__ == '__main__':
    database.Base.metadata.create_all(bind=database.engine)