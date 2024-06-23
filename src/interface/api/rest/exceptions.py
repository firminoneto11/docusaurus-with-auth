from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse

from conf import settings


class RedirectException(HTTPException):
    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to
        super().__init__(status_code=status.HTTP_307_TEMPORARY_REDIRECT)


async def redirect_exception_handler(request: Request, exc: RedirectException):
    url = settings.SERVER_URL + exc.redirect_to
    return RedirectResponse(url=url, status_code=exc.status_code)
