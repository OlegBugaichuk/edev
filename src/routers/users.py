from core.depends import get_db
from fastapi import APIRouter, Depends
from models.users import User as UserModel, Role as RoleModel
from schemas.users import (
    User as UserSchema, Role as RoleSchema, UserCreate, RoleCreate
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/users/', tags=["users"], response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()
    
@router.post('/users/', tags=["users"], response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get('/roles/', tags=["roles"], response_model=list[RoleSchema])
def get_roles(db: Session = Depends(get_db)):
    return db.query(RoleModel).all()


@router.post('/roles/', tags=["roles"], response_model=RoleSchema)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = RoleModel(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role