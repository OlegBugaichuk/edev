from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from core.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .schemas import User, UserCreate, UserLogin
from .helpers import check_user_password

from . import crud


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[User])
async def get_list_users(db:Session = Depends(get_db)):
    return crud.get_users(db)


@router.post('/', response_model=User, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    return new_user


@router.post('/login', status_code=200)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    result = await check_user_password(db, user.email, user.password)
    if result:
        return JSONResponse(content={'detail': 'Login success'})
    else:
        return HTTPException(status_code=401, detail='Email or password not valid')