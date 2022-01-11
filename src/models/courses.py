from core.databases import Base
from sqlalchemy import String, Integer, Column, ForeignKey, Float, Table
from sqlalchemy.orm import relationship


user_courses = Table('user_courses', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('course_id', ForeignKey('courses.id'), primary_key=True),
    Column('sort', Integer)
)

user_lesson_done = Table('user_lesson_done', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('course_id', ForeignKey('courses.id'), primary_key=True),
    Column('lesson_id', ForeignKey('lessons.id'), primary_key=True),
)


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(200))
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='author_courses')

    modules = relationship('Module', back_populates='course')
    students = relationship(
        'User', 
        secondary=user_courses, 
        back_populates='courses'
    )
    

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    description = Column(String(100))
    price = Column(Float)
    sort = Column(Integer)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='modules')

    lessons = relationship('Lesson', back_populates='module')


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    description = Column(String(100))
    duration_hours = Column(Integer)
    duration_minutes = Column(Integer)
    content = Column(String)
    sort = Column(Integer)
    module_id = Column(Integer, ForeignKey('modules.id'))
    module = relationship('Module', back_populates='lessons')

    users_done = relationship(
        'User', 
        secondary=user_lesson_done, 
        back_populates='lessons_done'
    )