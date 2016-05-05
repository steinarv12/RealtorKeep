import re
import requests
from bs4 import BeautifulSoup


def parseHTML(html):
    soup = BeautifulSoup(html, "html.parser")

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

        address = place.group(1)
        zipCode = place.group(3)
        price = re.search(r'[0-9]{2}\.[0-9]{3}\.[0-9]{3}',
                          str(about),
                          flags=re.UNICODE).group()
        squareMeters = re.search(r'([0-9]{2,3},[0-9])\sm',
                                 str(about),
                                 flags=re.UNICODE).group(1)
        rooms = re.search(r'([0-9])\s\w+\.',
                          str(about),
                          flags=re.UNICODE).group(1)
        type = re.search(r'>\s?(\w+)\s?<',
                         str(about),
                         flags=re.UNICODE).group(1)

        try:
            priceINT = int(price.replace(".", ""))
        except Exception, e:
            priceINT = -1

        return {"description": description,
                "rooms": rooms,
                "type": type,
                "m2": squareMeters,
                "price": priceINT,
                "address": address,
                "propertyID": propertyID,
                "pictureURL": pictureURL,
                "registrationDate": registrationDate,
                "zipCode": zipCode,
                "numberOfPages": numberOfPages}
