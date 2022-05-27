from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: str
    name: Union[str, None] = None
    created_at: datetime

    class Config:
        orm_mode = True



class ItemBase(BaseModel):
    title: str
    author: Union[str, None] = None
    category: List[str] = []
    publication_year: Union[int, None] = None
    description: Union[str, None] = None
    image_URL: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: str

    class Config:
        orm_mode = True