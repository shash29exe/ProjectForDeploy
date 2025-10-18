import asyncio

from aiogram import Bot, Dispatcher
from database.db import engine
from database.models import Base
from config import TOKEN
from handlers import router

async def main():
    Base.metadata.create_all(engine)
    bot = Bot(TOKEN, parse_mode=None)

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())