from aiogram import html
from aiogram.filters import Command
from aiogram.types import Message

from app.commands import get_default_commands
from app.routers import user_router as router
from database.models import User
from loader import _


@router.message(Command("start"))
async def _start(message: Message, user: User):
    commands = get_default_commands(user.lang)

    text = _('Hello <b>{}</b>').format(html.quote(message.from_user.full_name)) + "\n\n" + _("Commands:")
    for i in commands:
        text += f"\n{i.command} - {i.description.capitalize()}"
    await message.answer(text)