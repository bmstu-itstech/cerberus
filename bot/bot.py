import logging

from maxapi import Bot, Dispatcher

from common.config import Config
from common.di import HasContainer

from bot.handlers.container_middleware import ContainerMiddleware


logging.basicConfig(level=logging.DEBUG)


resolver = HasContainer()
config = resolver.resolve(Config)
bot = Bot(token=config.token)
dp = Dispatcher()
dp.outer_middlewares.append(ContainerMiddleware(container=resolver._container))


async def start_polling() -> None:
    from bot.handlers.start import on_start, on_bot_started
    from bot.handlers.search import search
    from bot.handlers.get import get
    from bot.handlers.team import team
    from bot.handlers.reports import report, infirmary, left, uspen

    await dp.start_polling(bot)
