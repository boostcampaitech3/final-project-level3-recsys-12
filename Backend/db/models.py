from datetime import datetime, timedelta, timezone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    # index는 query performance를 좋게 하기 위해 사용한다.
    hashed_password = Column(String, nullable=False)
    name = Column(String)

    def __str__(self):
        return self.id


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True)
    title = Column(String)
    publication_year = Column(Integer)
    description = Column(String)
    image_URL = Column(String)

    authors = relationship("BookAuthor", back_populates="book")
    genres = relationship("BookGenre", back_populates="book")

    def __str__(self):
        return self.title


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("BookGenre", back_populates="genre")

    def __str__(self):
        return self.name


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("BookAuthor", back_populates='author')

    def __str__(self):
        return self.name


class BookAuthor(Base):
    __tablename__ = "book_authors"
    book_id = Column(ForeignKey('books.id'), primary_key=True)
    author_id = Column(ForeignKey('authors.id'), primary_key=True)

    book = relationship("Book", back_populates="authors")
    author = relationship("Author", back_populates="books") 


class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id = Column(ForeignKey('books.id'), primary_key=True)
    genre_id = Column(ForeignKey('genres.id'), primary_key=True)

    book = relationship("Book", back_populates="genres")
    genre = relationship("Genre", back_populates="books")


class Rating(Base):
    __tablename__ = "ratings"
    user = Column(String, ForeignKey('users.id'), primary_key=True)
    item = Column(String, ForeignKey('books.id'), primary_key=True)
    rating = Column(Integer)


class UserQnA(Base):
    __tablename__ = 'user_qna'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    content = Column(Text)
    create_date = Column(DateTime)
    is_answered = Column(Boolean)


def default_loan_due():
    days_of_loan_term = 7
    due_date = datetime.now(timezone(timedelta(hours=9))) + timedelta(days=days_of_loan_term)
    return due_date


class Loan(Base):
    __tablename__ = 'loan_info'
    isbn = Column(String,  ForeignKey('books.id'), primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    due = Column(DateTime, default=default_loan_due)
    count = Column(Integer)
    is_return = Column(Boolean)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)