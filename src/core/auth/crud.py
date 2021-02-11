from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from src.core.settings import SECRET_KEY, ALGORITHM
from .helpers import pwd_context
from . import models, schemas
from .helpers import check_password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    '''
        Create user
    '''
    hashed_pass = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate_user(db: Session, email: str, password: str):
    '''
        Check password and return user or None
    '''
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        return None
    print(db_user.hashed_password)
    if not check_password(password, db_user.hashed_password):
        return None
    return db_user


async def get_current_user(db: Session, token: str):
    '''
    Return current user, using jwt
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception
    user = get_user(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user