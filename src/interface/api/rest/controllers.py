from fastapi import Request


class DocsController:
    @staticmethod
    async def get(): ...


class LoginController:
    @classmethod
    async def handle(cls, request: Request):
        if request.method.upper() == "GET":
            return cls.get()

        try:
            form_data = await request.body()
        except Exception as exc:
            # TODO: Return 400 html template
            raise exc

        return cls.post(form_data.decode())

    @staticmethod
    async def get(): ...

    @staticmethod
    async def post(form_data: str):
        print(form_data)
