from aiogram.types import BotCommand, BotCommandScopeDefault

from loader import _, bot, i18n


def get_default_commands(lang: str = "en"):
    commands = [
        BotCommand(command="/totp", description=_("get passwords", locale=lang)),
        BotCommand(command="/add_totp", description=_("add totp key", locale=lang)),
        BotCommand(command="/remove_totp", description=_("remove totp key", locale=lang)),
        BotCommand(command="/start", description=_("start chat", locale=lang)),
    ]

    return commands


async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_default_commands(lang), scope=BotCommandScopeDefault(), language_code=lang
        )
