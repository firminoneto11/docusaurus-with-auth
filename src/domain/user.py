from odmantic import Model


class User(Model):
    id: str
    username: str
    password: str
