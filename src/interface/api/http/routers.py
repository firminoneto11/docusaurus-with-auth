from dataclasses import dataclass

from fastapi import APIRouter, FastAPI, status
from fastapi.responses import HTMLResponse, StreamingResponse

from conf import settings

from .controllers import DocsController, LoginController


@dataclass
class ApplicationMount:
    path: str
    app: FastAPI
    name: str

    def __post_init__(self):
        self.version = self.path.replace("/", "")


def get_mounts():
    app_v1 = FastAPI(**settings.get_asgi_settings())

    app_v1.include_router(router, tags=["Core"])

    return [ApplicationMount(path="/v1", app=app_v1, name="v1")]


router = APIRouter()


router.add_api_route(
    path="/docs",
    methods=["GET"],
    response_class=StreamingResponse,
    endpoint=DocsController.get,
    status_code=status.HTTP_200_OK,
    name="core:docs",
    summary="SPA Documentation page",
)
router.add_api_route(
    path="/login",
    methods=["GET", "POST"],
    response_class=HTMLResponse,
    endpoint=LoginController.handle,
    status_code=status.HTTP_200_OK,
    name="core:login",
    summary="Login page",
)
