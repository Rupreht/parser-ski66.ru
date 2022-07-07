#!/usr/bin/env python

"""System modules."""
import json
import re
import sys
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
rep = [",", " ", "-", "'"]

ADDON_VALUE_DICT = {
    "Описание:": "descriptions",
    "Протоколы:": "protocols",
    "Фото:": "photos",
    "Впечатления:": "impressions",
    "Контакты:": "contacts"
}

fresh_events_dict = {}

def get_events(to_log=False) -> dict:
    """ Get Events """

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
    else:
        events_dict = {}

    req = requests.get("http://ski66.ru/app/", headers=headers)
    with open("data/index.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    soup = BeautifulSoup(req.text, "lxml")

    title = soup.title.text
    description = soup.find("meta", attrs={'name': 'Description'})["content"]

    events_dict["main"] = {
        "title": title,
        "description": description
    }

    table = soup.find(class_="table-bordered").find_all("tr")
    iteration_count = int(len(table))
    count = 1
    if to_log:
        print(f"Всего итераций: {iteration_count}")

    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Referer'] = 'http://ski66.ru/app/'

    for row in table:
        row_tds = row.find(class_="bg-confirm-start")
        if row_tds is not None:
            tds = row.find_all("td")
            date = tds[0].get_text("|").replace(" ", "").replace("|", " ").replace("\n", "")
            data_id = tds[1]["data-id"]
            event_name = descdescript = re.sub(' +', ' ', tds[1].text.strip())

            if data_id in events_dict:
                continue

            # Mining a values: "Описание:" "Контакты:" "Протоколы:" "Фото:" "Впечатления:"
            req = requests.post("http://ski66.ru/app/cal",
                headers=headers, data=[('descr_id', data_id)])
            soup = BeautifulSoup(req.text.replace("\n", " "), "lxml")
            rdesc = soup.find_all(["h4", "a"])
            fdate = datetime.strptime(date.split()[1].strip("-"), '%d-%m-%Y').strftime('%Y-%m-%d')

            new_object_dict = {
                "description": typograf.processtext(descdescript),
                "src_date": date,
                "distances":
                    typograf.processtext(
                        re.sub(' +', ' ', tds[2].text.strip().replace(" км", "км"))
                    ),
                "sity": typograf.processtext(tds[3].text.strip()),
                "mode": tds[4].text.strip(),
                "date": fdate,
                "forward": False
            }

            for item in rdesc:
                if item.find() is not None:
                    if not item.text.strip():
                        continue
                    p_key = ADDON_VALUE_DICT[f"{item.text.strip()}"]
                    new_object_dict[p_key] = {}
                elif 'http' not in item.text:
                    new_object_dict[p_key].update({
                        f"{item.text.strip()}": item.get('href').strip()
                    })
            fresh_events_dict[data_id] = new_object_dict
            events_dict[data_id] = new_object_dict

            for item in rep:
                if item in event_name:
                    event_name = event_name.replace(item, "_")

            with open(f"data/{fdate}-{data_id}-{event_name}.json",
                "w", encoding="utf-8") as file:
                json.dump(events_dict[data_id], file, indent=4, ensure_ascii=False)

            if to_log:
                print(f"# Итерация {count}. [{new_object_dict['description']}] записан...")
            sleep(random.randrange(3, 6))

        count += 1
        iteration_count = iteration_count - 1
        if to_log:
            print(f"Осталось итераций: {iteration_count}")

    with open(FILE_EVENTS_DICT, "w", encoding="utf-8") as file:
        json.dump(events_dict, file, indent=4, ensure_ascii=False)

    return fresh_events_dict

def main():
    """ Main """
    file_fresh_events_dict = "data/fresh_events_dict.json"
    fresh_events = get_events(True)
    _len = len(fresh_events)
    if _len > 0:
        print("Find: ", _len)
        with open(file_fresh_events_dict, "w", encoding="utf-8") as file:
            json.dump(fresh_events, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()

sys.exit(0)
