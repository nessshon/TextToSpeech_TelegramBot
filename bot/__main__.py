import asyncio
import logging

from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import Unauthorized

from bot.commands import start_command
from bot.handlers import tts_handler
from bot.loader import dp
from bot.throttling import ThrottlingMiddleware


async def main():
    logging.basicConfig(
        format=u'#%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.INFO
    )
    dp.setup_middleware(ThrottlingMiddleware())

    dp.register_message_handler(
        start_command, CommandStart()
    )
    dp.register_message_handler(
        tts_handler, content_types='text'
    )

    try:
        await dp.start_polling()
    except Unauthorized:
        logging.error('Неверный токен!')
    finally:
        await (await dp.bot.get_session()).close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logging.error('Бот остановлен!')
