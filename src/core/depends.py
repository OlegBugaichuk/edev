from crud.users_crud import UserCRUD
from fastapi import Depends, Header, HTTPException
from models.users import User
from schemas.users import Token
from sqlalchemy.orm import Session

from core.security import decode_jwt

from .databases import SessionLocal


def get_db() -> Session:
    with SessionLocal() as db:
        yield db
    
def get_token(token: str = Header(None)) -> Token:
    if not token:
        raise HTTPException(status_code=403, detail='Need a token')
    
    data = token.split(' ')
    if data[0] != 'Bearer':
        raise HTTPException(status_code=403, detail='Token error')
    
    return Token(type=data[0], token=data[1])

def current_user(token: Token = Depends(get_token)) -> User:
    try:
        user_id = decode_jwt(token.token)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=e)

    db = next(get_db())
    user = UserCRUD().get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=403, detail='Token error')
    return user
