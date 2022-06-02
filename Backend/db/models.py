import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from db.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    # index는 query performance를 좋게 하기 위해 사용한다.
    hashed_password = Column(String, nullable=False)
    name = Column(String)

    rating_user = relationship("Rating", back_populates="user_info")
    inference_user = relationship('Inference', back_populates="user_info")

    def __str__(self):
        return self.id


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True)
    title = Column(String)
    publication_year = Column(Integer)
    publisher = Column(String)
    synopsis = Column(String)
    image_URL = Column(String)

    authors = relationship("BookAuthor", back_populates="book")
    genres = relationship("BookGenre", back_populates="book")
    loan_book = relationship("Loan", back_populates="book")
    rating_item = relationship("Rating", back_populates="item_info")
    inference_item = relationship('Inference', back_populates="item_info")

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

    user_info = relationship("User", back_populates="rating_user")
    item_info = relationship("Book", back_populates="rating_item")


class UserQnA(Base):
    __tablename__ = 'user_qna'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    content = Column(Text)
    create_at = Column(DateTime)
    is_answered = Column(Boolean)


class Loan(Base):
    __tablename__ = 'loan_info'
    book_id = Column(String,  ForeignKey('books.id'), primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    loan_at = Column(DateTime, primary_key = True)
    return_at = Column(DateTime)
    due = Column(DateTime)
    count = Column(Integer)
    is_return = Column(Boolean)

    book = relationship("Book", back_populates="loan_book")


class Inference(Base):
    __tablename__ = 'inference'
    item = Column(String,  ForeignKey('books.id'), primary_key=True)
    user = Column(String, ForeignKey('users.id'), primary_key=True)
    score = Column(Numeric(precision=10, scale=7))

    user_info = relationship("User", back_populates="inference_user")
    item_info = relationship("Book", back_populates="inference_item")

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)