from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str
    db_name: str = 'edev'
    db_user: str = 'edev'
    db_pass: str
    db_host: str = 'localhost'
    db_port: int = 5432

@lru_cache
def get_settings() -> Settings:
    return Settings()