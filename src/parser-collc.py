#!/usr/bin/env python

import fitz
import re

pdf_file="data/kalendar2022leto.pdf"
pattern = re.compile("(.*)\n")
start_parse = False
with fitz.open(pdf_file) as doc:
    for page in doc.pages():
        for num, item in enumerate(pattern.findall(page.get_text("bloks"))):
            if start_parse:
                print(f"{num} {item}")
            if "Ответственный" in item:
                start_parse = True
