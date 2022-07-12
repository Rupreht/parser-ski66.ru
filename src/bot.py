""" TgBot """
import json
import asyncio
import logging
from os import getenv
from typing import List
from datetime import datetime
import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, executor, types
from lib.common import add_utm_tracking

# from aiogram.dispatcher.filters import Text
# from aiofiles import os

bot = Bot(token=getenv('TOKEN_BOT'), parse_mode='MarkdownV2')
dispatcher = Dispatcher(bot)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

FILE_FRESH_EVENTS_DICT="data/fresh_events_dict.json"

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
            text += fmt.escape_md(' | ')
        else:
            text += fmt.text('', '\n')
        count += 1
    return text

def clean_fresh_events_dict() -> None:
    """ Clear Fresh events """
    with open(FILE_FRESH_EVENTS_DICT, "w", encoding="utf-8") as file:
        json.dump({}, file)

def get_fresh_events(pub=False) -> List:
    """ Get Fresh events """
    with open(FILE_FRESH_EVENTS_DICT, "r", encoding="utf-8") as file:
        fresh_events_dict = json.load(file)
    events = []
    # exception_mode = ['Бег по шоссе, трейлы', 'Легкая атлетика']
    exception_mode = []
    events_name_dict = {
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

        for item, name_ru in events_name_dict.items():
            if fresh_events_dict[i][item]:
                text += fmt.text(fmt.text('', '\n'),
                    fmt.bold(name_ru), fmt.text('', '\n'))
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

start_buttons = ['/test', '/test2', '/fresh_events']
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add(*start_buttons)

@dispatcher.message_handler(commands='start')
async def start(message: types.Message):
    """ Start bot """
    await message.answer('Test msg', reply_markup=keyboard)

@dispatcher.message_handler(commands='fresh_events')
async def fresh_events(message: types.Message):
    """ Test sendMessage """
    user_id = message.from_id
    for text in get_fresh_events():
        await bot.send_message(user_id, text,
            disable_web_page_preview=True,
            disable_notification=True,
            reply_markup=keyboard)
        await asyncio.sleep(2)

@dispatcher.message_handler(commands='pub_fresh_events')
async def pub_fresh_events():
    """ Test sendMessage """
    for text in get_fresh_events(pub=True):
        # Post to channel "Спортивные события лыжников УрФО" https://t.me/SkiUral
        await bot.send_message(-1001511845683, text,
            disable_web_page_preview=True)
        await asyncio.sleep(1)
    clean_fresh_events_dict()

@dispatcher.message_handler(commands='clean_fresh_events')
async def clean_fresh_events(message: types.Message):
    """ Clean Fresh Events """
    clean_fresh_events_dict()
    await message.answer(fmt.escape_md('Clean Fresh Events'))

async def cron_fresh_events():
    """ Test sendMessage """
    user_id = getenv("USER_ID")
    start_strf = datetime.today().strftime("%A, %d. %B %Y %I:%M%p")
    bot.send_message(user_id, f"{start_strf} Start CRON",
                disable_web_page_preview=True, disable_notification=True)
    while True:
        for text in get_fresh_events():
            await bot.send_message(user_id, text,
                disable_web_page_preview=True, disable_notification=True)
            await asyncio.sleep(2)
        clean_fresh_events_dict()
        await asyncio.sleep(3600*3)

async def async_main():
    """ Async Main """
    loop = asyncio.get_running_loop()
    loop.create_task(cron_fresh_events())

def main() -> None:
    """ Main """
    executor.start_polling(dispatcher)
    asyncio.run(async_main())

if __name__ == '__main__':
    main()
