from datetime import datetime

import punq

from maxapi.enums import TextFormat
from maxapi.filters.command import Command
from maxapi.types import MessageCreated

from bot.bot import dp
from bot.logic.usecases import GetGlobalReport, GetInfirmaryReport, \
    GetUspenReport, GetLeftReport
from .templates import render


@dp.message_created(Command("report"))
async def report(event: MessageCreated, container: punq.Container) -> None:
    rep = container.resolve(GetGlobalReport)()
    await event.message.answer(
        render(
            "global_report.j2",
            now=datetime.now(),
            total=rep.total,
            camp=rep.camp,
            infirmary=rep.infirmary,
            left=rep.left,
        ),
        format=TextFormat.HTML,
    )


@dp.message_created(Command("infirmary"))
async def infirmary(event: MessageCreated, container: punq.Container) -> None:
    rep = container.resolve(GetInfirmaryReport)()
    await event.message.answer(
        render(
            "infirmary_report.j2",
            now=datetime.now(),
            participants=rep.participants,
        ),
        format=TextFormat.HTML,
    )


@dp.message_created(Command("left"))
async def left(event: MessageCreated, container: punq.Container) -> None:
    rep = container.resolve(GetLeftReport)()
    await event.message.answer(
        render(
            "left_report.j2",
            now=datetime.now(),
            participants=rep.participants,
        ),
        format=TextFormat.HTML,
    )


@dp.message_created(Command("uspen"))
async def uspen(event: MessageCreated, container: punq.Container) -> None:
    rep = container.resolve(GetUspenReport)()
    await event.message.answer(
        render(
            "uspen_report.j2",
            now=datetime.now(),
            participants=rep.participants,
        ),
        format=TextFormat.HTML,
    )
