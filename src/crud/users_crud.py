from models.users import Role, User
from schemas.users import UserCreate, RoleCreate
from sqlalchemy.orm import Session
from core.security import get_password_hash


class UserCRUD:
    
    def get_users(self, db: Session) -> list[User]:
        return db.query(User).all()
    
    def create(self, user: UserCreate, db: Session) -> User:
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        user_db = User(**user.dict())
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db


class RoleCRUD:

    def get_roles(self, db: Session) -> list[Role]:
        return db.query(Role).all()
    
    def create(self, role: RoleCreate, db: Session) -> Role:
        role_db = Role(**role.dict())
        db.add(role_db)
        db.commit()
        db.refresh(role_db)
        return role_db

