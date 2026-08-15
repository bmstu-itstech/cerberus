import punq
from maxapi.enums import TextFormat
from maxapi.filters.command import Command
from maxapi.types import MessageCreated

from bot.bot import dp
from bot.logic.usecases import SearchParticipants
from .templates import render

from .utils import strip_command


@dp.message_created(Command("s"))
@dp.message_created(Command("search"))
async def search(event: MessageCreated, container: punq.Container) -> None:
    if not event.message.body:
        return
    q = strip_command(event.message.body.text or "")
    res = container.resolve(SearchParticipants)(q)
    await event.message.answer(
        render("search_results.j2", participants=res),
        format=TextFormat.HTML,
    )
