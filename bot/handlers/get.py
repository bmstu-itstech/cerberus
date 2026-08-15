import punq
from maxapi.enums import TextFormat
from maxapi.filters.command import Command
from maxapi.types import MessageCreated

from bot.bot import dp
from bot.logic.usecases import GetParticipant
from .templates import render

from .utils import strip_command
from ..infra.repository import ParticipantNotFoundException


@dp.message_created(Command("g"))
@dp.message_created(Command("get"))
async def get(event: MessageCreated, container: punq.Container) -> None:
    if not event.message.body:
        return

    q = strip_command(event.message.body.text or "")
    if not q:
        await event.message.answer(
            render("get_command_invalid_usage.j2"),
            format=TextFormat.HTML,
        )
        return

    try:
        _id = int(q)
    except ValueError:
        await event.message.answer(
            render("get_command_invalid_id.j2", id=q),
            format=TextFormat.HTML,
        )
        return

    try:
        p = container.resolve(GetParticipant)(_id)
    except ParticipantNotFoundException:
        await event.message.answer(
            render("participant_not_found.j2", id=_id),
            format=TextFormat.HTML,
        )
        return

    await event.message.answer(
        render("participant_info.j2", p=p),
        format=TextFormat.HTML,
    )
