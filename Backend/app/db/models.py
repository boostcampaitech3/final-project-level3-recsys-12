from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    age = Column(Integer)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Item(Base):
    __tablename__ = "items"

    isbn = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    publication_year = Column(Integer)
    image_URL = Column(String)


