from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI

from conf import settings
from shared.types import ASGIApp
from src.infra.db import get_db_adapter

from .exceptions import RedirectException, redirect_exception_handler
from .middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import get_routers


@asynccontextmanager
async def lifespan(app: ASGIApp):
    await app.state.db.connect()
    yield
    app.state.db.disconnect()


def get_asgi_application():
    kwargs = settings.get_asgi_settings(main_mount=True)

    application = FastAPI(**kwargs, lifespan=lifespan)
    application.state.db = get_db_adapter()

    application.add_middleware(**allowed_hosts_middleware_configuration)
    application.add_middleware(**cors_middleware_configuration)

    application.state._mounted_applications = []
    for router in get_routers():
        application.mount(path=router.path, app=router.app, name=router.name)
        application.state._mounted_applications.append(router)

    application.add_exception_handler(RedirectException, redirect_exception_handler)

    return cast(ASGIApp, application)


app = get_asgi_application()
