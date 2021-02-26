from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from typing import List

from src.core.db.database import get_db
from .depends import oauth2_scheme
from .schemas import User, UserCreate
from .helpers import get_current_user
from . import crud


router = APIRouter()


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


@router.delete("/{user_id}")
async def read_users_me(user_id:int, db:Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    current_user = await get_current_user(db, token)
    if current_user:
        crud.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=User)
async def read_users_me(db:Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    current_user = await get_current_user(db, token)
    return current_user