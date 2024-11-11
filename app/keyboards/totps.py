from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import _
from database.models import UserTotpKey


class TotpsCallback(CallbackData, prefix="totps"):
    secret: str


def get_totps_markup(totps: list[UserTotpKey]):
    builder = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=i.name, callback_data=TotpsCallback(secret=i.secret).pack()) for i in totps]
    builder.add(*buttons)
    builder.adjust(2)

    return builder.as_markup()
