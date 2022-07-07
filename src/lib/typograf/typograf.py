"""Parse Text """
import json
import urllib.parse
import requests

class Typograf:
    """
        typograf.py
        python-implementation of ArtLebedevStudio.Typograf class (web-service client)

        Copyright (c) Art. Lebedev Studio | http://www.artlebedev.ru/

        Typograf homepage: http://typograf.artlebedev.ru/
        Web-service address: http://typograf.artlebedev.ru/webservices/typograf.asmx
        WSDL-description: http://typograf.artlebedev.ru/webservices/typograf.asmx?WSDL

        Default charset: UTF-8
        attr:
            entity:
                0 - готовыми символами
                2 - буквенными кодами
                3 - числовыми кодами
            rm_tab:
                1 - удалять символы табуляции
            spc_punct:
                1 - убирать и ставить пробелы до/после знаков препинания
            afterScan:
                1 - почистить текст после сканирования
            parser:
                1 - текст для «Парсера»
    """

    _doTypa = 1
    _quote_1 = 1
    _quote_2 = 2
    _entity = 0
    _rm_tab = 0
    _spc_punct = 1
    _afterscan = 1
    _parser = 0
    _encoding = 'UTF-8'

    def __init__(self, encoding='UTF-8', attr=None) -> None:
        self._encoding = encoding

        if "entity" in attr:
            self._entity = attr["entity"]
        if "rm_tab" in attr:
            self._rm_tab = 1
        if "spc_punct" in attr:
            self._spc_punct = 1
        if "afterScan" in attr:
            self._afterscan = 1
        if "parser" in attr:
            self._parser = 1

    def htmlentities(self):
        """htmlEntities"""
        self._entity = 1

    def xmlentities(self):
        """xmlEntities"""
        self._entity = 2

    def mixedentities(self):
        """mixedEntities"""
        self._entity = 4

    def noentities(self):
        """noEntities"""
        self._entity = 3

    # def br(self, value):
    #     if value:
    #         self._useBr = 1
    #     else:
    #         self._useBr = 0

    # def p(self, value):
    #     if value:
    #         self._useP = 1
    #     else:
    #         self._useP = 0

    # def nobr(self, value):
    #     if value:
    #         self._maxNobr = value
    #     else:
    #         self._maxNobr = 0

    def processtext(self, text) -> str:
        """ Text processer """
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        _headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.artlebedev.ru",
            "Referer": "https://www.artlebedev.ru/typograf/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        _data = {
            "doTypa": self._doTypa,
            "msg": text,
            "quote_1": self._quote_1,
            "quote_2": self._quote_2,
            "entity": self._entity,
        }

        if self._rm_tab != 0:
            _data["rm_tab"] = self._rm_tab

        if self._spc_punct != 0:
            _data["spc_punct"] = self._spc_punct

        if self._afterscan != 0:
            _data["afterScan"] = self._afterscan

        if self._parser != 0:
            _data["parser"] = self._parser

        data = urllib.parse.urlencode(_data)

        typografresponse = requests.post("https://www.artlebedev.ru/typograf/ajax.html",
            headers=_headers, data=data)

        try:
            res = str(json.loads(typografresponse.text)["typographed"])
        except JSONDecodeError:
            res = text
            pass

        return res
