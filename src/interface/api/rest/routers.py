from dataclasses import dataclass

from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import HTMLResponse

from conf import settings

from .controllers import DocsController, LoginController
from .middleware import redirect_middleware


@dataclass
class ApplicationMount:
    path: str
    app: FastAPI
    name: str


def get_routers():
    app_v1 = FastAPI(**settings.get_asgi_settings())

    app_v1.include_router(router)

    return [ApplicationMount(path="/v1", app=app_v1, name="v1")]


router = APIRouter(tags=["Core"])


router.add_api_route(
    path="/documentation",
    methods=["GET"],
    response_class=HTMLResponse,
    endpoint=DocsController.get,
    status_code=200,
    name="core:index",
    summary="SPA index page",
    dependencies=[Depends(redirect_middleware)],
)
router.add_api_route(
    path="/login",
    methods=["GET", "POST"],
    response_class=HTMLResponse,
    endpoint=LoginController.handle,
    status_code=200,
    name="core:login",
    summary="Login page",
    dependencies=[Depends(redirect_middleware)],
)
