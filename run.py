from aiogram import Bot, Dispatcher
import asyncio
from config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await dp.start_polling(bot)

    if __name__ == '__main__':
        asyncio.run(main())
