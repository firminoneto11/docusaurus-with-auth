from shared.utils import get_env

from .base import BaseSettings

with (env := get_env()).prefixed(BaseSettings.ENVIRONMENT_PREFIX):

    class Settings(BaseSettings):
        ENVIRONMENT = "production"
        DATABASE_URL = env.str("DATABASE_URL")
        ALLOWED_HOSTS = env.str("ALLOWED_HOSTS").split(",")
        ALLOWED_ORIGINS = env.str("ALLOWED_ORIGINS").split(",")
        DEBUG = False

        DOCS_URL = None
        REDOC_URL = None
        OPENAPI_URL = None
