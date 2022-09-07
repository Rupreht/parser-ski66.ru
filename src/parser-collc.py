#!/usr/bin/env python

"""
Parser for http://collc.narod.ru
Insatll:
    pip install fitz PyMuPDF
"""

# import re
from os.path import exists
import requests
import fitz

PDF_FILE="data/kalendar2022leto.pdf"

if not exists(PDF_FILE):
    request = requests.get("http://collc.narod.ru/pologenia/kalendar2022leto.pdf",
        allow_redirects=True)
    open(PDF_FILE, 'wb').write(request.content)

event = {
    "data": "",  # 1
    "title": "", # 2
    "sity": ""   # 3
}

# pattern = re.compile("\,\n")
# pattern = re.compile("(\d+)\s\s(\d+\.\d+\.\d+)\s\n(.+\s.+\s.+)")

# Start_Parse = False
# with fitz.open(PDF_FILE) as doc:
#     num = 0
#     print(doc.metadata['modDate'])
#     for page in doc.pages():
#         for num, text in enumerate(pattern.split(page.get_text())):
#             text = text.strip('\n')
#             print(f"[{num}] [{text}]")
#             # if Start_Parse:
#             #     print(f"{num} {item}")
#             #     if num % 2:
#             #         print(f"data: {item}")
#             #     num += 1
#             # if "Ответственный" in item:
#             #     Start_Parse = True

with fitz.open(PDF_FILE) as doc:
    print(doc)
    for page in doc.pages():
        print(page.get_text("text"))
