from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True)
    title = Column(String)
    publication_year = Column(Integer)
    description = Column(String)
    image_URL = Column(String)

    authors = relationship("BookAuthor", back_populates="book")
    genres = relationship("BookGenre", back_populates="genre")

    def __str__(self):
        return self.title


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


class Rating(Base):
    __tablename__ = "ratings"
    user = Column(String, ForeignKey('users.id'), primary_key=True)
    item = Column(String, ForeignKey('books.id'), primary_key=True)
    rating = Column(Integer)


