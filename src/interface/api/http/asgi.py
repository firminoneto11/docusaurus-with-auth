from contextlib import asynccontextmanager
from functools import partial
from typing import cast

from fastapi import FastAPI

from conf import settings
from shared.types import ASGIApp
from src.application.usecases.core import is_logged_in
from src.infra.db import get_db_adapter

from .middleware import (
    RedirectMiddleware,
    RedirectProxyPathMiddleware,
    RedirectToDocumentationPageMiddleware,
    allowed_hosts_middleware_configuration,
    correlation_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import get_mounts


@asynccontextmanager
async def lifespan(app: ASGIApp):
    await app.state.db.connect()
    yield
    app.state.db.disconnect()


class ASGIApplication:
    _created_apps: list["ASGIApp"] = []

    @classmethod
    def new(cls):
        application = cls().application
        cls._created_apps.append(application)
        return application

    @classmethod
    def latest_app(cls):
        return cls._created_apps[-1]

    def __init__(self):
        self.application = cast(
            ASGIApp,
            FastAPI(**settings.get_asgi_settings(main_mount=True), lifespan=lifespan),
        )

        self.setup_state()
        self.register_middleware()

    def setup_state(self):
        self.application.state.db = get_db_adapter()
        self.application.state._mounted_applications = []

        for mount in get_mounts():
            self.application.mount(path=mount.path, app=mount.app, name=mount.name)
            self.application.state._mounted_applications.append(mount)

    def register_middleware(self):
        RedirectMiddleware._is_logged_in = partial(
            is_logged_in, self.application.state.db.create_session
        )

        self.application.add_middleware(**cors_middleware_configuration)
        self.application.add_middleware(**allowed_hosts_middleware_configuration)
        self.application.add_middleware(**correlation_middleware_configuration)
        self.application.add_middleware(RedirectToDocumentationPageMiddleware)
        self.application.add_middleware(RedirectMiddleware)
        self.application.add_middleware(RedirectProxyPathMiddleware)


app = ASGIApplication.new()
