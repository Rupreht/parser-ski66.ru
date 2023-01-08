""" cron tg bot """
from os import getenv
import sqlite3
from datetime import datetime, timedelta
import requests

TOKEN = getenv('TOKEN_BOT')
CHAT_ID = getenv('CHAT_ID')
con = sqlite3.connect("file:data/db.sqlite?mode=rw", uri=True)
cur = con.cursor()
date_now = datetime.now().date()
date_delta = timedelta(days=31)
res = cur.execute(f"""SELECT id, pub_date, title, content, forward
    FROM
        post
    WHERE 1
        and pub_date BETWEEN '{date_now}' AND '{date_delta + date_now}'
        and forward==1""")

def get_request(url):
    try:
        req = requests.get(url, timeout=5)
        if req.status_code != 200:
            print(f"error: {req.status_code}")
            return False
        result = req.json()
        return result
    except:
        return False

for item in res.fetchall():
    URL = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}"
        "&disable_web_page_preview=1"
        "&parse_mode=MarkdownV2"
        f"&text={requests.utils.quote(item[3])}")
    if get_request(URL):
        cur.execute(f"UPDATE post SET forward=2 WHERE id={item[0]}")
        con.commit()

con.close()
