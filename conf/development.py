from .base import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT = "development"
    DATABASE_URL = "mongodb://localhost:27017/"
    ALLOWED_HOSTS = ["*"]
    ALLOWED_ORIGINS = ["*"]
    DEBUG = True
    SERVER_URL = "http://localhost:8000"
