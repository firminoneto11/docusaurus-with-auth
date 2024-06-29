from .base import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT = "development"
    DATABASE_URL = "mongodb://root:password@localhost:27017/"
    ALLOWED_HOSTS = ["*"]
    ALLOWED_ORIGINS = ["*"]
    DEBUG = True
