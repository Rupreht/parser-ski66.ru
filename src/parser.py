#!/usr/bin/env python

"""System modules."""
import sys
from time import sleep
import random

# Dependent modules.
import requests
from bs4 import BeautifulSoup

URL = "http://ski66.ru/app/"
URL_DESCRIPT = "http://ski66.ru/app/cal"

headers = {
    "Accept": '*/*',
    "User-Agent": \
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
    "Connection": 'keep-alive',
    "Upgrade-Insecure-Requests": '1'
}

req = requests.get(URL, headers=headers)
src = req.text

with open("data/index.html", "w", encoding="utf-8") as file:
    file.write(src)

# with open("index.html", encoding="utf-8") as file:
    # src = file.read()

soup = BeautifulSoup(src.replace("\n", " "), "lxml")

# title = soup.title.text
# DESCRIPTION = soup.find("meta", attrs={'name': 'Description'})["content"]

# print(title)
# print(DESCRIPTION)

table = soup.find(class_="table-bordered").find_all("tr")
iteration_count = int(len(table))
COUNT = 1
print(f"Всего итераций: {iteration_count}")

headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Referer'] = 'http://ski66.ru/app/'

for row in table:
    row_tds = row.find(class_="bg-confirm-start")
    if row_tds is not None:
        tds = row.find_all("td")
        date = tds[0].get_text("|").replace(" ", "").replace("|", " ")
        data_id = tds[1]["data-id"]
        descdescript = tds[1].text.strip()
        distances = tds[2].text.strip()
        sity = tds[3].text.strip()
        mode = tds[4].text.strip()
        req = requests.post(URL_DESCRIPT, headers=headers, data=[('descr_id', data_id)])
        # with open(f"data/get-descr-{data_id}.html", encoding="utf-8") as file:
            # src = file.read().replace("\n", " ")
        src = req.text
        with open(f"data/{data_id}-descr.html", "w", encoding="utf-8") as file:
            file.write(src)
        soup = BeautifulSoup(src.replace("\n", " "), "lxml")
        rdesc = soup.find_all(["h4", "a"])
        DESCRIPTION = ''
        for item in rdesc:
            if item.find() is not None:
                DESCRIPTION += f"{item.text.strip()}\n"
            elif 'http' not in item.text:
                DESCRIPTION += f"<a href=\"{item.get('href')}\">{item.text.strip()}</a>\n"

        with open(f"data/{data_id}-{date}-descr.txt", "a", encoding="utf-8") as file:
            file.write(f"{date} | {descdescript} | {distances} | {sity} | {mode}\n")
            file.write(DESCRIPTION)

        print(f"# Итерация {COUNT}. {descdescript} записан...")
        sleep(random.randrange(2, 4))

    COUNT += 1
    iteration_count = iteration_count - 1
    print(f"Осталось итераций: {iteration_count}")
sys.exit(0)
