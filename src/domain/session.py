from odmantic import Model


class Session(Model):
    id: str
    user_id: str
