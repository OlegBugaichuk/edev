from pydantic import BaseModel
from typing import Optional


class UserTypeBase(BaseModel):
    title: str


class UserTypeCreate(UserTypeBase):
    pass


class UserType(UserTypeBase):
    id: int
    
    class Config:
        orm_mode = True
    

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = False
    is_admin: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[str] = None
    phone: Optional[str] = None
    user_type: Optional[UserType] = None

    class Config:
        orm_mode = True


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None