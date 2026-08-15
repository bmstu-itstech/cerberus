import punq
from maxapi.enums import TextFormat
from maxapi.filters.command import Command
from maxapi.types import MessageCreated

from bot.bot import dp
from bot.logic.usecases import GetTeam
from .templates import render

from .utils import strip_command


@dp.message_created(Command("t"))
@dp.message_created(Command("team"))
async def team(event: MessageCreated, container: punq.Container) -> None:
    if not event.message.body:
        return
    q = strip_command(event.message.body.text or "")
    try:
        team_ = int(q)
    except ValueError:
        team_ = 0
    data = container.resolve(GetTeam)(team_)
    await event.message.answer(
        render(
            "team_info.j2",
            team=team_,
            district=data.district,
            curators=data.curators,
            participants=data.participants,
        ),
        format=TextFormat.HTML,
    )
