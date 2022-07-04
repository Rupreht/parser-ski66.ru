from os import getenv
import loggings
# from async_main import collect_data
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os

bot = Bot(token=getenv('TOKEN_BOT'))
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Moscow', 'Ekaterinburg']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Please select a City', reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)
