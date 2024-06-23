from datetime import datetime, timezone
from functools import lru_cache
from typing import TYPE_CHECKING, Literal, overload
from uuid import uuid4

from environs import Env

if TYPE_CHECKING:
    from .types import ASGIApp


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env


def generate_uuid():
    return str(uuid4())


@overload
def utc_timestamp(unix: Literal[True]) -> int: ...


@overload
def utc_timestamp(unix: Literal[False]) -> datetime: ...


def utc_timestamp(unix: bool = False):
    utc_now = datetime.now(tz=timezone.utc)
    if unix:
        utc_now = int(utc_now.timestamp())
    return utc_now


def reverse_url(application: "ASGIApp", controller_name: str, version: str, **kwargs):
    for mount in application.state._mounted_applications:
        for route in mount.app.routes:
            if route.name == controller_name:
                return mount.path + route.url_path_for(controller_name, **kwargs)

    raise AttributeError(f"The version {version!r} wasn't mounted in the application")
