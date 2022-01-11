from pydantic import BaseModel


class Role(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    title: str


class UserBase(BaseModel):
    email: str
    first_name: str
    second_name: str
    last_name: str
    phone: str
    age: int


class User(UserBase):
    id: int
    role: Role

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    role_id: int
