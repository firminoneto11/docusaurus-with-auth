from fastapi import Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from src.application.usecases.core import proxy_to_server

from .utils import redirect, render, umount_request


class DocsController:
    @classmethod
    async def get(cls, request: Request):
        data = await umount_request(request=request)
        response = await proxy_to_server(**data)

        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=response.headers,
            background=BackgroundTask(response.aclose),
        )


class LoginController:
    @classmethod
    async def handle(cls, request: Request):
        if request.method.upper() == "GET":
            return await cls.get()
        return await cls.post(request)

    @staticmethod
    async def get():
        return render("login.html")

    @staticmethod
    async def post(request: Request):
        try:
            form_data = await request.form()
        except:  # noqa
            return render("400.html")

        username = form_data.get("username")
        password = form_data.get("password")

        print(username, password)

        # CHECK PASSWORD
        # INVALIDATE PREVIOUS SESSION
        # CREATE NEW SESSION
        # SET IN THE COOKIE

        return redirect("core:docs", raise_=True)
