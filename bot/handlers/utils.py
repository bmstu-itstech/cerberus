import punq
from typing import Any


def strip_command(s: str) -> str:
    i = s.find(" ")
    if i < 0:
        return ""
    return s[i + 1 :]


def container(data: dict[str, Any]) -> punq.Container:
    return data["container"]
