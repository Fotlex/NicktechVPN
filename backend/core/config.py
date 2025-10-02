from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str

    DEBUG: bool
    TIMEZONE: str

    ALLOWED_HOSTS: list[str]
    CSRF_TRUSTED_ORIGINS: list[str]
    DJANGO_SECRET_KEY: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB_CELERY: str
    REDIS_DB_FSM: str
    REDIS_DB_CACHE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()