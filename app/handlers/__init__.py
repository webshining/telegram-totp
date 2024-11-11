from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message

from utils import logger

from .users import router as user_router


def setup_handlers(dp: Dispatcher) -> None:
    @dp.error()
    async def _error(event: ErrorEvent):
        logger.exception(event.exception)

    @dp.message(Command('cancel'))
    async def _cancel(message: Message, state: FSMContext):
        await message.delete()
        await state.set_state(None)

    dp.include_routers(user_router)
