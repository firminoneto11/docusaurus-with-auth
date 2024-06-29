from typing import TYPE_CHECKING, Awaitable, Callable, Optional

from asgi_correlation_id.middleware import CorrelationIdMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware

from conf import settings

from .utils import redirect, umount_request

if TYPE_CHECKING:
    from fastapi import Request
    from starlette.middleware.base import RequestResponseEndpoint


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
    "expose_headers": ["X-Request-ID"],
}

correlation_middleware_configuration = {
    "middleware_class": CorrelationIdMiddleware,
}


class RedirectToDocumentationPageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: "Request", call_next: "RequestResponseEndpoint"):
        if request.url.path == "/":
            return redirect("core:docs")

        return await call_next(request)


class RedirectMiddleware(BaseHTTPMiddleware):
    _is_logged_in: Callable[[Optional[str]], Awaitable[bool]]

    @property
    def is_logged_in(self):
        return RedirectMiddleware._is_logged_in

    async def dispatch(self, request: "Request", call_next: "RequestResponseEndpoint"):
        session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
        is_authenticated = await self.is_logged_in(session_id)

        if request.url.path == "/v1/login" and is_authenticated:
            return redirect("core:docs")

        if request.url.path == "/v1/docs" and (not is_authenticated):
            return redirect("core:login")

        return await call_next(request)


class RedirectProxyPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: "Request", call_next: "RequestResponseEndpoint"):
        path = request.url.path

        if path == "/proxy-server":
            return redirect("core:docs")

        if "/proxy-server" in path:
            return await self._proxy_to_server(request=request)

        return await call_next(request)

    async def _proxy_to_server(cls, request: "Request"):
        from src.application.usecases.core import proxy_to_server

        data = await umount_request(request=request)

        data["path"] = data["path"].replace("/proxy-server", "")

        response = await proxy_to_server(**data)

        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=response.headers,
            background=BackgroundTask(response.aclose),
        )
