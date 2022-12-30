"""System modules."""
import re
from time import sleep
import random
from datetime import datetime
import aiogram.utils.markdown as fmt

# Dependent modules.
import requests
import app
from bs4 import BeautifulSoup

# from app import db, create_app
from app.src.lib.common import add_utm_tracking
from app.posts.models import Post

_app = app.create_app()
_app.app_context().push()

ADDON_VALUE_DICT = {
    "Описание:": "descriptions",
    "Протоколы:": "protocols",
    "Фото:": "photos",
    "Впечатления:": "impressions",
    "Контакты:": "contacts"
}

events_name_dict = {
    "descriptions": "Описание:",
    "protocols": "Протоколы:",
    "photos": "Фото:",
    "impressions": "Впечатления:",
    "contacts": "Контакты:"
}

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


def get_events() -> None:
    """
    Get Events
    """

    headers = {
        "Accept": '*/*',
        "User-Agent": \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
        "Connection": 'keep-alive',
        "Upgrade-Insecure-Requests": '1'
    }

    soup = BeautifulSoup(
        requests.get("http://ski66.ru/app/", headers=headers).text, "lxml")

    for row in soup.find(class_="table-bordered").find_all("tr"):
        if row.find(class_="bg-confirm-start") is not None:
            tds = row.find_all("td")
            date = tds[0].get_text("|").replace(" ", "").replace("|", " ").replace("\n", "")
            data_id = tds[1]["data-id"]
            event_name = descdescript = re.sub(' +', ' ', tds[1].text.strip())
            fdate = datetime.strptime(date.split()[1].strip("-"), '%d-%m-%Y').strftime('%Y-%m-%d')

            post = Post.query.filter_by(title = f"{date} {descdescript}-{data_id}").first()

            if post is not None:
                continue

            new_object_dict = {
                "description": descdescript,
                "src_date":    date,
                "distances":   re.sub(' +', ' ', tds[2].text.strip().replace(" км", "км")),
                "sity":        tds[3].text.strip(),
                "mode":        tds[4].text.strip(),
                "date":        fdate
            }

            new_object_dict = get_add_info(data_id, new_object_dict)

            for item in [",", " ", "-", "'"]:
                if item in event_name:
                    event_name = event_name.replace(item, "_")

            # with open(f"data/{fdate}-{data_id}.json", "w", encoding="utf-8") as file:
            #     json.dump(events_dict[data_id], file, indent=4, ensure_ascii=False)

            text = fmt.text(
                fmt.escape_md(new_object_dict['src_date']),
                fmt.bold(new_object_dict['description']), fmt.text('', '\n'),
                fmt.bold('дистанция:'),
                    fmt.escape_md(new_object_dict['distances']), fmt.text('', '\n'),
                fmt.bold('место:'), fmt.escape_md(new_object_dict['sity']), fmt.text('', '\n'),
                fmt.bold('вид:'), fmt.escape_md(new_object_dict['mode']), fmt.text('', '\n')
            )

            for item, name_ru in events_name_dict.items():
                if new_object_dict[item]:
                    text += fmt.text(fmt.text('', '\n'),
                        fmt.bold(name_ru), fmt.text('', '\n'))
                    text = print_links_to_cols(new_object_dict[item], text)

            text += fmt.text(
                fmt.text('', '\n'),
                fmt.link("@SkiUral", "https://t.me/SkiUral"),
                fmt.escape_md(" | "),
                fmt.link('ski66©', add_utm_tracking('http://ski66.ru', utm_params)),
                fmt.text('', '\n')
                )


            post = Post(
                title = f"{new_object_dict['src_date']} {new_object_dict['description']}-{data_id}",
                content  = text,
                ovner = 2000
                )

            post.set_pub_date(new_object_dict['date'])
            post.set_sity(new_object_dict['sity'])

            app.db.session.add(post)
            app.db.session.commit()
            print(f"Save new post: {post.title}\n")

            # import sys
            # sys.exit()

            sleep(random.randrange(3, 6))

    return None


def get_add_info(data_id, new_object_dict):
    """ Get Add Info """

    headers = {
        "Accept": "*/*",
        "User-Agent": \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "http://ski66.ru/app/",
    }

    # values : "Описание:" "Контакты:" "Протоколы:" "Фото:" "Впечатления:"
    req = requests.post("http://ski66.ru/app/cal",
        headers=headers, data=[('descr_id', data_id)], timeout=5)
    soup = BeautifulSoup(req.text.replace("\n", " "), "lxml")
    rdesc = soup.find_all(["h4", "a"])

    for item in rdesc:
        if item.find() is not None:
            if not item.text.strip():
                continue
            p_key = ADDON_VALUE_DICT[item.text.strip()]
            new_object_dict[p_key] = {}
        elif 'http' not in item.text:
            new_object_dict[p_key].update({
                item.text.strip(): item.get('href').strip()
            })

    return new_object_dict

if __name__ == '__main__':
    get_events()
