from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str
    db_name: str = 'edev'
    db_user: str = 'edev'
    db_pass: str
    db_host: str = '127.0.0.1'
    db_port: int = 5432

    def get_database_uri(self) -> str:
        return f'postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

@lru_cache
def get_settings() -> Settings:
    return Settings()