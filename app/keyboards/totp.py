from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import _


class TotpCallback(CallbackData, prefix="totp"):
    action: str


def get_totp_markup():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=_("Add"), callback_data=TotpCallback(action="add").pack()))
    builder.row(InlineKeyboardButton(text=_("Remove"), callback_data=TotpCallback(action="remove").pack()))
    builder.row(InlineKeyboardButton(text=_("Refresh"), callback_data=TotpCallback(action="refresh").pack()))

    return builder.as_markup()
