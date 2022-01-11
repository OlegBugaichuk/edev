from core.databases import Base
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from .courses import user_courses, user_lesson_done


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    title = Column(String(15))
    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(320))
    password = Column(String)
    first_name = Column(String(20))
    second_name = Column(String(20))
    last_name = Column(String(20))
    phone = Column(String(15))
    age = Column(Integer)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")

    author_courses = relationship('Course', back_populates='author')

    courses = relationship(
        'Course', 
        secondary=user_courses, 
        back_populates='students'
    )

    lessons_done = relationship(
        'Lesson', secondary=user_lesson_done, back_populates='users_done'
    )