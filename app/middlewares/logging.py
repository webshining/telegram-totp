from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update, CallbackQuery, Message

from utils import logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        if event.message:
            self._message(event.message)
        elif event.callback_query:
            self._callback(event.callback_query)
        return await handler(event, data)

    @staticmethod
    def _message(message: Message):
        logger.debug(f'Received message [ID:{message.message_id}] from user [ID:{message.from_user.id}] '
                     f'in chat [ID:{message.chat.id}] text "{message.text}"')

    @staticmethod
    def _callback(callback_query: CallbackQuery):
        logger.debug(f'Received callback query [data:"{callback_query.data}"] '
                     f'from user [ID:{callback_query.from_user.id}] '
                     f'for message [ID:{callback_query.message.message_id}] '
                     f'in chat [ID:{callback_query.message.chat.id}]')