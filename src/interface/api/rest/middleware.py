from typing import Optional

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from conf import settings

from .exceptions import RedirectException

allowed_hosts_middleware_configuration = {
    "middleware_class": TrustedHostMiddleware,
    "allowed_hosts": settings.ALLOWED_HOSTS,
}


cors_middleware_configuration = {
    "middleware_class": CORSMiddleware,
    "allow_origins": settings.ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


async def _is_logged_in(session_id: Optional[str]) -> bool: ...


async def redirect_middleware(request: Request):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    authenticated = await _is_logged_in(session_id=session_id)
    path = request.url

    if "/login" in path and authenticated:
        raise RedirectException(redirect_to="/documentation")

    if "/documentation" in path and not authenticated:
        raise RedirectException(redirect_to="/login")
