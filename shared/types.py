from typing import TYPE_CHECKING, Literal, Protocol

from fastapi import FastAPI
from starlette.datastructures import State

type EnvChoices = Literal["development", "testing", "staging", "production"]

if TYPE_CHECKING:
    from src.infra.db.db_adapter import DBAdapter


class _ApplicationMountProtocol(Protocol):
    path: str
    app: FastAPI
    name: str
    version: str


class _CustomAppState(State):
    db: "DBAdapter"
    _mounted_applications: list[_ApplicationMountProtocol]


class ASGIApp(FastAPI):
    state: _CustomAppState
