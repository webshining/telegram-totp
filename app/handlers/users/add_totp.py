import cv2
import io
import numpy as np
from pyzbar.pyzbar import decode
from urllib.parse import urlparse, parse_qs

from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext

from app.routers import user_router as router
from database.models import User, UserTotpKey
from loader import _, bot
from app.states import TotpState
from utils import send_message_with_delete


def decode_qr(image_data: bytes) -> str | None:
    image = np.frombuffer(image_data, dtype=np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    decoded_objects = decode(img)

    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    else:
        return None


def parse_totp_uri(uri: str):
    parsed_uri = urlparse(uri)
    params = parse_qs(parsed_uri.query)

    secret = params.get("secret", [None])[0]
    digits = params.get("digits", [6])[0]
    period = params.get("period", [30])[0]

    return {"secret": secret, "digits": digits, "period": period}


@router.message(Command("add_totp"))
async def _add_totp(message: Message, state: FSMContext):
    await send_message_with_delete(message, text=_("Enter name:"), state=state, skip_first=not message.text.startswith("/"))
    await state.set_state(TotpState.name)


@router.message(TotpState.name)
async def _add_totp_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await send_message_with_delete(message, text=_("Send qr code:"), state=state)
    await state.set_state(TotpState.key)


@router.message(TotpState.key, lambda message: message.content_type == ContentType.PHOTO)
async def _add_totp_key(message: Message, state: FSMContext, user: User):
    data = await state.get_data()

    await message.delete()
    await bot.delete_messages(message.chat.id, data.get("messages_to_delete"))
    await state.clear()

    photo = await bot.download(file=message.photo[-1].file_id, destination=io.BytesIO())
    qr_uri = decode_qr(photo.read())
    if not qr_uri:
        return await message.answer(_("QR code not found"))

    qr_data = parse_totp_uri(qr_uri)
    qr_data["name"] = data.get("name")
    keys = [k.model_dump() for k in user.keys]
    keys.append(UserTotpKey(**qr_data).model_dump())
    await User.update(user.id, keys=keys)

    await message.answer(_("Key added"))
