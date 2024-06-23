from .development import Settings as DevSettings


class Settings(DevSettings):
    ENVIRONMENT = "testing"
