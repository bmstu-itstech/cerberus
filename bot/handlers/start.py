from maxapi import F
from maxapi.enums import TextFormat
from maxapi.filters.command import CommandStart
from maxapi.types import MessageCreated, BotStarted

from bot.bot import dp, bot

from .templates import render


@dp.bot_started()
async def on_bot_started(event: BotStarted) -> None:
    await bot.send_message(
        user_id=event.user.user_id,
        text=render("on_bot_started.j2"),
        format=TextFormat.HTML,
    )


@dp.message_created(CommandStart())
async def on_start(event: MessageCreated) -> None:
    await event.message.answer(
        text=render("on_start.j2"),
        format=TextFormat.HTML,
    )
