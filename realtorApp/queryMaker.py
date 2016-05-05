import requests
from realtorApp.models import RealEstate as RE
from realtorApp.htmlParser import parseHTML


def makeQuery(paramObject):
    r = requests.get("http://fasteignir.visir.is/ajaxsearch/getresults",
                     params=paramObject)
    if r.status_code == 200:
        return (r.text, r.url)
    else:
        return None


def getParams(pageNumber):
    if pageNumber is None:
        pageNumber = 1
    zipCodes = {'zip': '103,104,105,107,108,109,110,111,112,113,200,201,202,210,170'}
    areaFrom = '80'
    areaTo = '150'
    area = {'area': areaFrom + ',' + areaTo}
    catagories = {'category': '1,2,4,7'}
    tags = {'tag': 'entrance_private&timespan=7'}
    type = {'stype': 'sale'}
    priceFrom = '27000000'
    priceTo = '35000000'
    price = {'price': priceFrom + ',' + priceTo}
    roomsFrom = '3'
    roomsTo = '6'
    rooms = {'room': roomsFrom + ',' + roomsTo}
    page = {'page': pageNumber}

    params = {**zipCodes, **area, **catagories, **tags, **type,
              **price, **rooms, **page}

    return params


def handleParsedOutput(parsedObjectList):
    for parsedObject in parsedObjectList:
        try:
            listing = RE.objects.get(siteID=parsedObject['propertyID'])
        except RE.DoesNotExist:
            listing = RE(street=parsedObject['address'],
                         price=parsedObject['price'],
                         postDate=parsedObject['registrationDate'],
                         rooms=parsedObject['rooms'],
                         area=parsedObject['area'],
                         zip=parsedObject['zipCode'],
                         type=parsedObject['type'],
                         description=parsedObject['description'],
                         siteID=parsedObject['propertyID'],
                         pictures=parsedObject['pictureURL'])
        else:
            if (listing.price > parsedObject['price']
                and parsedObject['price'] != -1):
                listing.price = parsedObject['price']
                # TODO - notify
        try:
            listing.save()
        except Exception as e:
            raise


def controlFlow():
    paramObject = getParams(None)

    queryObject = makeQuery(paramObject)
    if queryObject is None:
        return "Error connecting to API"

    parsedObjectList = parseHTML(queryObject[0])
    handleParsedOutput(parsedObjectList)

    for i in range(2, parsedObjectList[0]['numberOfPages'] + 1):
        paramObject = getParams(i)
        queryObject = makeQuery(paramObject)
        parsedObjectList = parseHTML(queryObject[0])
        handleParsedOutput(parsedObjectList)

    return "success"
