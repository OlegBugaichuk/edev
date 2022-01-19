from core.depends import current_user, get_db
from core.security import create_access_token, verify_password
from crud.users_crud import RoleCRUD, UserCRUD
from fastapi import APIRouter, Depends, HTTPException
from schemas.users import LoginSchema
from schemas.users import Role as RoleSchema
from schemas.users import RoleCreate, Token
from schemas.users import User as UserSchema
from schemas.users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/users/', tags=["users"], response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return UserCRUD().get_users(db)


@router.post('/users/me/', tags=["users"], response_model=UserSchema)
def my_profile(current_user: UserSchema = Depends(current_user)):
    return current_user


@router.get('/users/{user_id}/', tags=["users"], response_model=UserSchema)
def get_users(user_id:int, db: Session = Depends(get_db)):
    user = UserCRUD().get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/users/', tags=["users"], response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserCRUD().create(user, db)


@router.get('/roles/', tags=["roles"], response_model=list[RoleSchema])
def get_roles(db: Session = Depends(get_db)):
    return RoleCRUD().get_roles(db)


@router.post('/roles/', tags=["roles"], response_model=RoleSchema)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return RoleCRUD().create(role, db)


@router.post('/login/', tags=['auth'], response_model=Token)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = UserCRUD().get_user_by_email(data.email, db)
    if user and verify_password(data.password, user.password):
        token = create_access_token(user.id)
        return Token(token=token)
    else:
        raise HTTPException(status_code=401)
