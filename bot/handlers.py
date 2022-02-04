import asyncio
import os

from aiogram import types
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.utils.markdown import hcode, hbold
from gtts import gTTS

from bot.throttling import rate_limit


@rate_limit(3)
async def tts_handler(message: types.Message):
    sticker = 'CAACAgIAAxkBAAIsnmGMc6Xnxqz-T5IZJGrMO6_HY04QAAJBAQACzRswCPHwYhjf9pZYIgQ'
    action = types.ChatActions.RECORD_AUDIO
    limit = 500

    if len(message.text) <= limit:

        try:
            await message.answer_chat_action(action=action)
            msg = await message.answer_sticker(sticker=sticker)

            voice_path = f'{message.from_user.id}.ogg'
            gTTS(text=message.text, lang='ru', slow=False).save(voice_path)

            await message.answer_voice(
                voice=types.InputFile(voice_path),
            )
            await msg.delete()
            os.remove(voice_path)

        except (AssertionError, RuntimeError, ValueError):
            message_text = 'Произошла ошибка, попробуйте снова.'
            msg = await message.answer(message_text)

            await asyncio.sleep(3)
            await msg.delete()

        except (FileNotFoundError, MessageToDeleteNotFound):
            pass

    else:
        text = (
            f'{hbold("Обрезанный текс в " + str(limit) + " символов:")}\n\n'
            f'{hcode(message.text)}\n\n'
            f'{hbold("Превышен лимит символов!")}\n\n'
            f'Лимит символов: {hbold(str(limit))}\n'
            f'Всего символов в тексте: {hbold(str(len(message.text)))}\n\n'
        )
        await message.reply(text=text)
