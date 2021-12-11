from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from environs import Env

env = Env()
env.read_env()
memory_storage = MemoryStorage()

token = env.str("BOT_TOKEN")
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=memory_storage)
