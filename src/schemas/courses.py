from pydantic import BaseModel
from .users import User

class Course(BaseModel):
    id: int
    title: str
    description: str
    author: User


class Module(BaseModel):
    id: int
    title: str
    description: str
    course: Course
    price: float


class Lesson(BaseModel):
    id: int
    title: str
    description: str
    duration_hours: int
    duration_minutes: int
    content: str
    module: Module