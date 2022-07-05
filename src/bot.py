""" TgBot """
import json
import asyncio
import logging
import aiogram.utils.markdown as fmt
from os import getenv
from typing import List
from aiogram import Bot, Dispatcher, executor, types
from lib.common import add_utm_tracking

# from aiogram.dispatcher.filters import Text
# from aiofiles import os

bot = Bot(token=getenv('TOKEN_BOT'), parse_mode='MarkdownV2')
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

utm_params = {
    'utm_source': 'telegram',
    'utm_medium': 'channel_SkiUral',
    'utm_content': 'link',
}

def print_links_to_cols(array, text) -> str:
    """ Print Links to cols """
    count = 1
    size = len(array)
    for key in array:
        text += fmt.link(key, add_utm_tracking(array[key], utm_params))
        if count % 2 == 0:
            text += fmt.text('', '\n')
        elif size != count:
            text += fmt.escape_md('|')
        else:
            text += fmt.text('', '\n')
        count += 1
    return text

def get_fresh_events(pub=False) -> List:
    """ Get Fresh events """
    with open("data/fresh_events_dict.json", "r", encoding="utf-8") as file:
        fresh_events_dict = json.load(file)
    events = []
    # exception_mode = ['Бег по шоссе, трейлы', 'Легкая атлетика']
    exception_mode = []
    events_dict = {
        "descriptions": "Описание:",
        "protocols": "Протоколы:",
        "photos": "Фото:",
        "impressions": "Впечатления:",
        "contacts": "Контакты:"
    }

    for i in fresh_events_dict:
        # skip a running events
        if 'mode' not in fresh_events_dict[i]:
            continue
        if any(fresh_events_dict[i]['mode'] in s for s in exception_mode):
            continue
        # skip public posts
        if fresh_events_dict[i]['forward']:
            continue

        text = fmt.text(
            fmt.escape_md(fresh_events_dict[i]['src_date']),
            fmt.bold(fresh_events_dict[i]['description']), fmt.text('', '\n'),
            fmt.bold('дистанция:'),
                fmt.escape_md(fresh_events_dict[i]['distances']), fmt.text('', '\n'),
            fmt.bold('место:'), fmt.escape_md(fresh_events_dict[i]['sity']), fmt.text('', '\n'),
            fmt.bold('вид:'), fmt.escape_md(fresh_events_dict[i]['mode']), fmt.text('', '\n')
        )

        for item in events_dict:
            if item in fresh_events_dict[i]:
                if fresh_events_dict[i][item]:
                    text += fmt.text(fmt.text('', '\n'),
                        fmt.bold(events_dict[item]), fmt.text('', '\n'))
                    text = print_links_to_cols(fresh_events_dict[i][item], text)

        text += fmt.text(
            fmt.text('', '\n'),
            fmt.link("@SkiUral", "https://t.me/SkiUral"),
            fmt.escape_md(" | "),
            fmt.link('ski66©', add_utm_tracking('http://ski66.ru', utm_params)),
            fmt.text('', '\n')
            )

        if pub:
            fresh_events_dict[i]['forward']=True
            with open("data/fresh_events_dict.json", "w", encoding="utf-8") as file:
                json.dump(fresh_events_dict, file, indent=4, ensure_ascii=False)

        events.append(text)

    return events

@dp.message_handler(commands='start')
async def start(message: types.Message):
    """ Start bot """
    start_buttons = ['/test', '/test2', '/fresh_events']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*start_buttons)
    await message.answer('Test msg', reply_markup=keyboard)

@dp.message_handler(commands='test')
async def test(message: types.Message):
    """ Test sendMessage """
    text = """суббота 09-07-2022
*Роллерный триатлон #RollerSkiTriathlon*
*дистанция:* 8км
*место:* Екатеринбург, УСБ Динамо
*вид:* Лыжные гонки

*Протоколы:*
[10-07-2021](https://myfinish.info/online.php?evid=3559)"""
    await message.answer(fmt.escape_md(text))

@dp.message_handler(commands='test2')
async def test2(message: types.Message):
    """ Test sendMessage """
    text = """
воскресенье 10-07-2022
*Пробег "Егоршинская десятка"*
*дистанция:* 10км, 5км, 2,5км, 1км
*место:* Артемовский, лб Снежинка
*вид:* Бег по шоссе, трейлы

*Описание:*
[2022](https://yadi.sk/i/O4rYm_0DUv4Z4g)
"""
    await message.answer(fmt.escape_md(text))

@dp.message_handler(commands='fresh_events')
async def fresh_events(message: types.Message):
    """ Test sendMessage """
    user_id = message.from_id
    for text in get_fresh_events():
        await bot.send_message(user_id, text,
            disable_web_page_preview=True,
            disable_notification=True)
        await asyncio.sleep(2)

@dp.message_handler(commands='pub_fresh_events')
async def pub_fresh_events(message: types.Message):
    """ Test sendMessage """
    for text in get_fresh_events(pub=True):
        # Post to channel "Спортивные события лыжников УрФО" https://t.me/SkiUral
        await bot.send_message(-1001511845683, text,
            disable_web_page_preview=True)
        await asyncio.sleep(1)


async def cron_fresh_events():
    """ Test sendMessage """
    user_id = getenv("USER_ID")
    while True:
        for text in get_fresh_events():
            print(text)
            await bot.send_message(user_id, text,
                disable_web_page_preview=True, disable_notification=True)
            await asyncio.sleep(2)
        await asyncio.sleep(3600)

def main() -> None:
    """ Main """
    loop = asyncio.get_event_loop()
    loop.create_task(cron_fresh_events())
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
