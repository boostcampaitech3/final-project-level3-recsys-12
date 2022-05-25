from typing import List, Optional

from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    user_id: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    age: Optional[int] = None # Union[int, None] = None
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

    class Config:
        orm_mode = True
        # data가 dict이 아니라도 ORM model 같은 속성을 가지는 객체를 읽을 수 있게 해준다.
        # id = data['id'] or id = data.id