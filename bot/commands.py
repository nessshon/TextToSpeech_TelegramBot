from aiogram import types
from aiogram.utils.markdown import hbold

from bot.throttling import rate_limit


@rate_limit(2)
async def start_command(message: types.Message):
    text = (
        f'Привет, {hbold(message.from_user.first_name)}!\n'
        f'Отправь мне текст:'
    )

    await message.answer(text=text)
