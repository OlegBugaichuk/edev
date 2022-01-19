from http.client import HTTPException
from passlib.hash import pbkdf2_sha256
import jwt
from .config import Settings, get_settings


ALGORITHM = "HS256"

Settings = get_settings()


def create_access_token(user_id: int) -> str:
    to_encode = {"sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, Settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(jwt_token: str) -> dict:
    payload = jwt.decode(jwt_token, Settings.secret_key, algorithms=[ALGORITHM])
    user_id = payload.get('sub')
    if user_id is None:
        raise ValueError('Token error')
    return int(user_id)
    

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)