import asyncio

from bot import bot


async def main() -> None:
    await bot.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
