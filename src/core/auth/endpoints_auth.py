from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta

from src.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from src.core.db.database import get_db
from .schemas import Token
from .helpers import create_access_token, authenticate_user


router = APIRouter()

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