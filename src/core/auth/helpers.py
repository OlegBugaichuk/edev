from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .import models


pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated='auto')


async def check_user_password(db: Session, user_email: str, password: str) -> bool:
    '''
        Checking password for user
    '''
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        return False

    return pwd_context.verify(password, user.hashed_password)