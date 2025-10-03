import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.core.settings")
import django

django.setup()

from backend.core.config import config
from bot.handlers import setup_handlers


async def main():
    storage = RedisStorage.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB_FSM}"
    )

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    setup_handlers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    asyncio.run(main())
