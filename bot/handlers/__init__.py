from aiogram import Dispatcher

from .start import router as start_router


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
