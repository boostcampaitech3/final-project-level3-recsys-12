from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel



class UserBase(BaseModel):
    id: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    age: Optional[int] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    pass


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    isbn: str
    title: str
    author: str
    publisher: str
    publication_year: int
    image_URL: Union[str, None] = None

    class Config:
        orm_mode = True