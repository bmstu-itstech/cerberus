from typing import Any, Awaitable, Callable

import attrs
import punq

from maxapi.filters.middleware import BaseMiddleware


@attrs.define(slots=True)
class ContainerMiddleware(BaseMiddleware):
    container: punq.Container

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[None]],
        event_object: Any,
        data: dict[str, Any],
    ) -> Any:
        data["container"] = self.container
        return await handler(event_object, data)
