""" Lib """
import urllib.parse

def add_utm_tracking(url: str, params: dict) -> str:
    """ Add UTM for tracking """
    result = {} | params
    url_obj = urllib.parse.urlparse(url)
    if url_obj.query:
        query_dict = dict(x.split("=") for x in url_obj.query.split("&"))
        result.update(query_dict)
    return str(url_obj._replace(query=urllib.parse.urlencode(result)).geturl())
