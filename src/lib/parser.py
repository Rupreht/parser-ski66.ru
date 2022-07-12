"""System modules."""
import json
import re
from time import sleep
import random
from datetime import datetime
from os.path import exists

# Dependent modules.
import requests
from bs4 import BeautifulSoup
from lib.typograf import Typograf

typograf = Typograf(attr={"rm_tab": 1})

FILE_EVENTS_DICT = "data/events_dict.json"

ADDON_VALUE_DICT = {
    "Описание:": "descriptions",
    "Протоколы:": "protocols",
    "Фото:": "photos",
    "Впечатления:": "impressions",
    "Контакты:": "contacts"
}

def get_events() -> dict:
    """ Get Events """

    events_dict = {}
    fresh_events_dict = {}

    headers = {
        "Accept": '*/*',
        "User-Agent": \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
        "Connection": 'keep-alive',
        "Upgrade-Insecure-Requests": '1'
    }

    if exists(FILE_EVENTS_DICT):
        with open(FILE_EVENTS_DICT, "r", encoding="utf-8") as file:
            events_dict = json.load(file)

    soup = BeautifulSoup(
        requests.get("http://ski66.ru/app/", headers=headers).text, "lxml")

    events_dict["main"] = {
        "title": soup.title.text,
        "description": soup.find("meta", attrs={'name': 'Description'})["content"]
    }

    for row in soup.find(class_="table-bordered").find_all("tr"):
        if row.find(class_="bg-confirm-start") is not None:
            tds = row.find_all("td")
            date = tds[0].get_text("|").replace(" ", "").replace("|", " ").replace("\n", "")
            data_id = tds[1]["data-id"]
            event_name = descdescript = re.sub(' +', ' ', tds[1].text.strip())
            fdate = datetime.strptime(date.split()[1].strip("-"), '%d-%m-%Y').strftime('%Y-%m-%d')

            if data_id in events_dict:
                continue

            new_object_dict = {
                "description": typograf.processtext(descdescript),
                "src_date":    date,
                "distances":   re.sub(' +', ' ', tds[2].text.strip().replace(" км", "км")),
                "sity":        tds[3].text.strip(),
                "mode":        tds[4].text.strip(),
                "date":        fdate,
                "forward":     False
            }

            new_object_dict = get_add_info(data_id, new_object_dict)
            fresh_events_dict[data_id] = new_object_dict
            events_dict[data_id] = new_object_dict

            for item in [",", " ", "-", "'"]:
                if item in event_name:
                    event_name = event_name.replace(item, "_")

            with open(f"data/{fdate}-{data_id}-{event_name}.json",
                "w", encoding="utf-8") as file:
                json.dump(events_dict[data_id], file, indent=4, ensure_ascii=False)

            sleep(random.randrange(3, 6))

    with open(FILE_EVENTS_DICT, "w", encoding="utf-8") as file:
        json.dump(events_dict, file, indent=4, ensure_ascii=False)

    return fresh_events_dict

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

    # Mining :) a values : "Описание:" "Контакты:" "Протоколы:" "Фото:" "Впечатления:"
    req = requests.post("http://ski66.ru/app/cal",
        headers=headers, data=[('descr_id', data_id)])
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

def get_and_save_new_events() -> int:
    """ Save new events """
    fresh_events = get_events()
    _len = len(fresh_events)
    if _len > 0:
        with open("data/fresh_events_dict.json", "w", encoding="utf-8") as file:
            json.dump(fresh_events, file, indent=4, ensure_ascii=False)
    return _len
