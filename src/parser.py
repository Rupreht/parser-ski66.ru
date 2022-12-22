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
from lib.RemoteTypograf import RemoteTypograf

typograf = RemoteTypograf(attr={"rm_tab": 1})

def get_events(to_log=False) -> dict:
    """ Get Events """

    headers = {
        "Accept": '*/*',
        "User-Agent": \
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
        "Connection": 'keep-alive',
        "Upgrade-Insecure-Requests": '1'
    }

    url = "http://ski66.ru/app/"
    url_descript = "http://ski66.ru/app/cal"
    file_events_dict = "data/events_dict.json"
    rep = [",", " ", "-", "'"]
    addon_value_dict = {
        "Описание:": "descriptions",
        "Протоколы:": "protocols",
        "Фото:": "photos",
        "Впечатления:": "impressions",
        "Контакты:": "contacts"
    }

    if exists(file_events_dict):
        with open(file_events_dict, "r", encoding="utf-8") as file:
            events_dict = json.load(file)
    else:
        events_dict = {}
    fresh_events_dict = {}

    req = requests.get(url, headers=headers)
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
            distances = tds[2].text.strip().replace(" км", "км")
            distances = re.sub(' +', ' ', distances)
            sity = tds[3].text.strip()
            mode = tds[4].text.strip()

            if data_id in events_dict:
                continue

            # Mining a values: "Описание:" "Контакты:" "Протоколы:" "Фото:" "Впечатления:"
            req = requests.post(url_descript, headers=headers, data=[('descr_id', data_id)])
            soup = BeautifulSoup(req.text.replace("\n", " "), "lxml")
            rdesc = soup.find_all(["h4", "a"])
            fdate = datetime.strptime(date.split()[1].strip("-"), '%d-%m-%Y').strftime('%Y-%m-%d')

            new_object_dict = {
                "description": typograf.processText(descdescript),
                "src_date": date,
                "distances": typograf.processText(distances),
                "sity": typograf.processText(sity),
                "mode": mode,
                "date": fdate,
                "forward": False
            }

            for item in rdesc:
                if item.find() is not None:
                    if not item.text.strip():
                        continue
                    p_key = addon_value_dict[f"{item.text.strip()}"]
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
                print(f"# Итерация {count}. {descdescript} записан...")
            sleep(random.randrange(2, 4))

        count += 1
        iteration_count = iteration_count - 1
        if to_log:
            print(f"Осталось итераций: {iteration_count}")

    with open(file_events_dict, "w", encoding="utf-8") as file:
        json.dump(events_dict, file, indent=4, ensure_ascii=False)

    return fresh_events_dict

def main():
    """ Main """
    file_fresh_events_dict = "data/fresh_events_dict.json"
    fresh_events_dict = get_events(True)
    _len = len(fresh_events_dict)
    if _len > 0:
        print("Find: ", _len)
        with open(file_fresh_events_dict, "w", encoding="utf-8") as file:
            json.dump(fresh_events_dict, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()

sys.exit(0)
