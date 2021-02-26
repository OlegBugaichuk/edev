from fastapi import Depends, HTTPException, status, APIRouter

from sqlalchemy.orm import Session
from typing import List

from src.core.db.database import get_db
from .schemas import UserType, UserTypeCreate
from . import crud

router = APIRouter()

@router.get("/", response_model=List[UserType])
async def get_list_user_types(db:Session = Depends(get_db)):
    return crud.get_user_types(db)


@router.post('/', response_model=UserType, status_code=201)
async def create_user_type(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    new_user_type = crud.create_user_type(db, user_type)
    return new_user_type


@router.get("/{user_type_id}", response_model=UserType)
async def get_user_type_detail(user_type_id: int, db: Session = Depends(get_db)):
    user_type = crud.get_user_type(db, user_type_id)
    if not user_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User type not found"
        )
    return user_type