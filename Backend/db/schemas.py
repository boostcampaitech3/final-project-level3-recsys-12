from typing import Optional

from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    id: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    name: Optional[str] = None # Union[int, None] = None

    class Config:
        orm_mode = True
        # data가 dict이 아니라도 ORM model 같은 속성을 가지는 객체를 읽을 수 있게 해준다.
        # id = data['id'] or id = data.id


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class BookBase(BaseModel):
    id: str
    title: str
    publication_year: Union[int, None] = None
    description: Union[str, None] = None
    image_URL: Union[str, None] = None

class AuthorBase(BaseModel):
    id: int
    name: str

class GenreBase(BaseModel):
    id: int
    name: str


class BookSchema(BookBase):
    authors: List[AuthorBase] = []
    genres: List[GenreBase] = []
  


class Author(AuthorBase):
    books: List[BookBase] = []

class Genre(GenreBase):
    books: List[BookBase] = []