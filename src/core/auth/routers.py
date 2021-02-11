from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from core.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from src.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import User, UserCreate, UserLogin, Token
from .helpers import create_access_token
from .crud import authenticate_user, get_current_user

from . import crud


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


@router.get("/", response_model=List[User])
async def get_list_users(db:Session = Depends(get_db)):
    return crud.get_users(db)


@router.post('/', response_model=User, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    return new_user


# @router.post('/login', status_code=200)
# async def login(user: UserLogin, db: Session = Depends(get_db)):
#     result = await check_user_password(db, user.email, user.password)
#     if result:
#         return JSONResponse(content={'detail': 'Login success'})
#     else:
#         return HTTPException(status_code=401, detail='Email or password not valid')


@router.post("/token", response_model=Token)
async def login_for_access_token(db:Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(db:Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    current_user = await get_current_user(db, token)
    return current_user