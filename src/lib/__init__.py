r"""
:mod:`add_utm_tracking`
"""

import urllib.parse

__version__ = '0.0.1'
__all__ = ["add_utm_tracking", "remotetypograf"]
__author__ = 'Nikolay Ermolovich <git@rupreht.ru>'

def add_utm_tracking(url: str, params: dict) -> str:
    """ Add UTM for tracking """
    result = {} | params
    url_obj = urllib.parse.urlparse(url)
    if url_obj.query:
        query_dict = dict(x.split("=") for x in url_obj.query.split("&"))
        result.update(query_dict)
    return str(url_obj._replace(query=urllib.parse.urlencode(result)).geturl())
