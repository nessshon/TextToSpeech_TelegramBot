import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()

        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        if throttled.exceeded_count < 3:
            text = (
                '<b>⚠️ Флуд контроль! </b>\n\n'
                'Вы сможете озвучить текст через <b>{rate_limit}</b> секунд.'
            )
            await message.answer(text.format(rate_limit=throttled.rate))

        if throttled.exceeded_count > 3:
            text = (
                '<b>‼️ Флуд контроль! </b>\n\n'
                'Подождите <b>{rate_limit}</b> секунд!'
            )
            msg = await message.reply(text.format(rate_limit=throttled.rate))

            await asyncio.sleep(2)
            await msg.delete()

        delta = throttled.rate - throttled.delta
        await asyncio.sleep(delta)


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throt    tling_key', key)
        return func

    return decorator
