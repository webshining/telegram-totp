import pyotp
from datetime import datetime

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.routers import user_router as router
from app.keyboards import get_totp_markup, TotpCallback
from database.models import User
from loader import _

from .add_totp import _add_totp
from .remove_totp import _remove_totp


@router.message(Command("totp"))
async def _totp(message: Message, user: User):
    text = _get_totp_text(user)
    await message.answer(text, reply_markup=get_totp_markup())


@router.callback_query(TotpCallback.filter())
async def _totp_refresh(
    call: CallbackQuery, user: User, callback_data: TotpCallback, state: FSMContext
):
    await call.answer()
    text = _get_totp_text(user)
    if callback_data.action == "refresh":
        try:
            await call.message.edit_text(text=text, reply_markup=get_totp_markup())
        except:
            pass
    elif callback_data.action == "remove":
        await _remove_totp(call.message, user, state)
    else:
        await _add_totp(call.message, state)


def _get_totp_text(user: User):
    text = ""
    for key in user.keys:
        totp = pyotp.TOTP(key.secret, digits=key.digits, interval=key.period)
        time_remaining = str(totp.interval - datetime.now().timestamp() % totp.interval).split(".")[
            0
        ]
        text += f"<b>{key.name}</b>"
        text += "\n---------------------------------------------\n"
        text += f"<code>{totp.now()}</code>             {time_remaining}"
        text += _(" seconds left")
        text += "\n---------------------------------------------\n"
    return text or _("Empty")
