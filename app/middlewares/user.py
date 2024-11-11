from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update

from database.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        if event.message:
            from_user = event.message.from_user
        elif event.callback_query:
            from_user = event.callback_query.from_user
        else:
            from_user = event.inline_query.from_user
        user = await User.update_or_create(from_user.id, from_user.id, name=from_user.full_name,
                                           username=from_user.username)
        data['user'] = user
        return await handler(event, data)
