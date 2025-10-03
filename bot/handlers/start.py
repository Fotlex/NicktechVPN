from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import get_start_keyboard
from bot.utils.db import get_bot_settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    settings = await get_bot_settings()
    text = settings["start_message"]

    await message.answer(
        text,
        reply_markup=get_start_keyboard(settings["webapp_url"], settings["group_url"]),
        parse_mode=ParseMode.HTML,
    )
