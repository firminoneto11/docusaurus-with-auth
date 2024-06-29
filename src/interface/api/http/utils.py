from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse
from jinja2 import Environment, FileSystemLoader

from conf import settings


def redirect(to: str, raise_: bool = False):
    url = reverse_url(controller_name=to)

    if raise_:
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    return RedirectResponse(url=url)


def render(template: str, **kwargs):
    return jinja.get_template(template).render(**kwargs)


def reverse_url(controller_name: str, version: str = "v1", **kwargs):
    from .asgi import ASGIApplication

    for mount in ASGIApplication.latest_app().state._mounted_applications:
        if mount.version != version:
            continue

        for route in mount.app.routes:
            if route.name == controller_name:
                return mount.path + route.url_path_for(controller_name, **kwargs)

    raise AttributeError(f"The version {version!r} wasn't mounted in the application")


async def umount_request(request: Request):
    method = request.method
    path = request.url.path
    query = request.url.query.encode()
    headers = request.headers.raw
    try:
        body = await request.body()
    except:  # noqa
        body = b""

    return {
        "method": method,
        "path": path,
        "query": query,
        "headers": headers,
        "body": body,
    }


jinja = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR), autoescape=True)
