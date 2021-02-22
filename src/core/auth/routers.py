from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from core.db.database import SessionLocal
from src.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import User, UserCreate, Token, UserType, UserTypeCreate
from .helpers import create_access_token, authenticate_user, get_current_user
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


@router.get("/{user_id}/", response_model=User)
async def get_user_detail(user_id:int, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/types", response_model=List[UserType])
async def get_list_user_types(db:Session = Depends(get_db)):
    return crud.get_user_types(db)


@router.post('/types', response_model=UserType, status_code=201)
async def create_user_type(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    new_user_type = crud.create_user_type(db, user_type)
    return new_user_type


@router.get("/types/{user_type_id}", response_model=UserType)
async def get_user_type_detail(user_type_id: int, db: Session = Depends(get_db)):
    user_type = crud.get_user_type(db, user_type_id)
    if not user_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User type not found"
        )
    return user_type


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