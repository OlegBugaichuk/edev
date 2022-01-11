from sqlalchemy.orm import Session

from .databases import SessionLocal


def get_db() -> Session:
    with SessionLocal() as db:
        yield db
    