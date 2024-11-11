from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.routers import user_router as router
from app.keyboards import get_totps_markup, TotpsCallback
from database.models import User
from loader import _, bot
from utils import send_message_with_delete


@router.message(Command("remove_totp"))
async def _remove_totp(message: Message, user: User, state: FSMContext):
    text = _("Select totp to delete:") if user.keys else _("Empty")
    await send_message_with_delete(
        message=message,
        text=text,
        reply_markup=get_totps_markup(user.keys),
        state=state,
        skip_first=not message.text.startswith("/"),
    )


@router.callback_query(TotpsCallback.filter())
async def _totps_remove(
        call: CallbackQuery, user: User, callback_data: TotpsCallback, state: FSMContext
):
    data = await state.get_data()

    keys = list(filter(lambda k: k.secret != callback_data.secret, user.keys))
    await User.update(user.id, keys=[k.model_dump() for k in keys])

    await call.message.delete()
    await bot.delete_messages(call.message.chat.id, data.get("messages_to_delete"))
    await state.clear()

    await call.message.answer(_("Key deleted"))
