import requests


def makeBaseSiteQuery(id):
    baseUrl = "http://fasteignir.visir.is/property/" + id
    r = requests.get(baseUrl)
    if r.status_code == 200:
        return r.text
    else:
        return None


def makePropertyQuery(paramObject):
    r = requests.get("http://fasteignir.visir.is/ajaxsearch/getresults",
                     params=paramObject)
    if r.status_code == 200:
        return (r.text, r.url)
    else:
        return None
