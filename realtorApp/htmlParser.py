import re
from bs4 import BeautifulSoup
from datetime import datetime
from realtorApp.querys import makeBaseSiteQuery


def parseHTML(html):
    soup = BeautifulSoup(html, "html.parser")

    propertyList = []

    realEstates = soup.findAll("div", {"class": "b-products-item-list"})
    numberOfPages = len(soup.find("p", {"id": "tracker-action-page-bottom"}).getText().split())
    for estate in realEstates:
        about = estate.find("div", {"class": "b-products-item-details-param"})
        descriptor = estate.findAll("p", {"class": "b-products-item-details-descr"})
        description = descriptor[0].getText()
        registrationDate = descriptor[1].getText()
        propertyID = re.search(r'property/([0-9]+)\?', str(estate)).group(1)
        pictureURL = re.search(r'http://api-beta.fasteignir.is/pictures/' +
                               propertyID + r'.+\.jpg',
                               str(estate)).group(0)

        place = re.search(r'>(\w+)(.+,|,)\s<span>([0-9]{3}\s\w+)<',
                          str(estate), flags=re.UNICODE)

        try:
            address = place.group(1)
        except Exception:
            address = "NOTFOUND"

        try:
            zipCode = place.group(3)
        except Exception:
            zipCode = "NOTFOUND"

        try:
            price = re.search(r'[0-9]{2}\.[0-9]{3}\.[0-9]{3}',
                              str(about),
                              flags=re.UNICODE).group()
        except Exception:
            price = -1

        try:
            squareMeters = re.search(r'([0-9]{2,3},?[0-9]?)\sm.<',
                                     str(about)).group(1)
        except Exception:
            squareMeters = -1

        try:
            rooms = re.search(r'([0-9])\s\w+\.',
                              str(about),
                              flags=re.UNICODE).group(1)
        except Exception:
            rooms = -1

        try:
            type = re.search(r'>\s?(\w+)\s?<',
                             str(about),
                             flags=re.UNICODE).group(1)
        except Exception:
            type = "NOTFOUND"

        if type.lower() == "tilboð":
            continue

        try:
            priceINT = int(price.replace(".", ""))
        except Exception:
            priceINT = -1

        registrationDate = registrationDate[9:]
        registrationDate = datetime.strptime(registrationDate, "%d.%m.%Y")
        squareMeters = squareMeters.replace(",", ".")
        detailedHTML = makeBaseSiteQuery(propertyID)
        deSoup = BeautifulSoup(detailedHTML, "html.parser")
        deDescription = deSoup.find('div', {"class": "description"})
        if deDescription is not None:
            description = str(deDescription)

        propertyList.append({"description": description,
                             "rooms": rooms,
                             "type": type,
                             "area": squareMeters,
                             "price": priceINT,
                             "address": address,
                             "propertyID": propertyID,
                             "pictureURL": pictureURL,
                             "registrationDate": registrationDate,
                             "zipCode": zipCode,
                             "numberOfPages": numberOfPages})

    return propertyList


def parseImageURLs(html):
    soup = BeautifulSoup(html, "html.parser")
    pictureList = []
    picContainer = soup.find("div", {"class": "image-tiles"})
    pics = picContainer.find_all('img', {"class": "lazyload"})
    for pic in pics:
        pictureList.append(pic.get('data-src'))
    return pictureList
