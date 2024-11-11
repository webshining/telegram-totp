from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def send_message_with_delete(message: Message, text: str, state: FSMContext, reply_markup = None, skip_first: bool = False):
    data = await state.get_data()
    answer_message = await message.answer(text=text, reply_markup=reply_markup)
    messages_to_delete = [*(data.get("messages_to_delete") or []), answer_message.message_id]
    if not skip_first:
        messages_to_delete.append(message.message_id)
    await state.update_data(messages_to_delete=messages_to_delete)
