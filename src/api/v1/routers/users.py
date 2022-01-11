from fastapi import APIRouter
from schemas.users import (
    User as UserSchema, Role as RoleSchema, UserCreate, RoleCreate
)
from crud.users_crud import UserCRUD, RoleCRUD
from sqlalchemy.orm import Session
from core.depends import get_db
from fastapi import Depends

router = APIRouter()


@router.get('/users/', tags=["users"], response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return UserCRUD().get_users(db)
    
@router.post('/users/', tags=["users"], response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserCRUD().create(user, db)


@router.get('/roles/', tags=["roles"], response_model=list[RoleSchema])
def get_roles(db: Session = Depends(get_db)):
    return RoleCRUD().get_roles(db)


@router.post('/roles/', tags=["roles"], response_model=RoleSchema)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return RoleCRUD().create(role, db)