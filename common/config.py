from os import getenv
from typing import Self

import attrs

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


@attrs.define(slots=True, frozen=True)
class Config(BaseSettings):
    token: str
    pg_dsn: PostgresDsn
    secret: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            token=getenv("MAX_BOT_TOKEN", ""),
            pg_dsn=PostgresDsn(getenv("POSTGRES_DSN", "")),
            secret=getenv("SECRET", ""),
        )
