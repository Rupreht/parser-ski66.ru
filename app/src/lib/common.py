""" Common defs """
import urllib.parse

def add_utm_tracking(url: str, params: dict) -> str:
    """ Add UTM for tracking """
    result = {} | params
    url_obj = urllib.parse.urlparse(url)
    if url_obj.query:
        try:
            result.update(
                dict(
                    x.split('=') for x in url_obj.query.split('&')
                    )
                )
        except ValueError:
            result = params

    return str(url_obj._replace(query=urllib.parse.urlencode(result)).geturl())
