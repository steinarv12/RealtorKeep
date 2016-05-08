import requests
from realtorApp.models import RealEstate as RE
from realtorApp.models import EstatePictures as EP
from realtorApp.htmlParser import parseHTML
from realtorApp.htmlParser import parseImageURLs
from realtorApp.compareImages import computeDiff as CD
from datetime import datetime
import uuid
from PIL import Image


def makePropertyQuery(paramObject):
    r = requests.get("http://fasteignir.visir.is/ajaxsearch/getresults",
                     params=paramObject)
    if r.status_code == 200:
        return (r.text, r.url)
    else:
        return None


def makeBaseSiteQuery(id):
    baseUrl = "http://fasteignir.visir.is/property/" + id
    r = requests.get(baseUrl)
    if r.status_code == 200:
        return r.text
    else:
        return None


def getImage(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        return Image.open(r.raw)
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
        isSameEstate = tuple()
        found = False
        try:
            listing = RE.objects.get(siteID=parsedObject['propertyID'])
        except RE.DoesNotExist:
            isSameEstate = isSameEstateByImage(parsedObject['propertyID'])
            if isSameEstate[0]:
                listing = RE.objects.get(siteID=isSameEstate[1])
                listing.previousPrice = listing.price
                listing.description = parsedObject['description']
                listing.modified = datetime.now()
            else:
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
            if (listing.price > parsedObject['price'] and
                parsedObject['price'] != -1):
                listing.modified = datetime.now()
                listing.previousPrice = listing.price
                listing.price = parsedObject['price']
                # TODO - notify
            found = True
        try:
            listing.save()
            if len(isSameEstate) > 0 and isSameEstate[0] is False and found is False:
                for image in isSameEstate[1]:
                    nameEnd = str(uuid.uuid1())
                    name = parsedObject['propertyID'] + '-' + nameEnd + '.jpg'
                    path = "estatePictures/" + name
                    try:
                        image.save(path)
                    except Exception as e:
                        print("first")
                        print(e)
                    finally:
                        image.close()
                    try:
                        newPic = EP(estatePicture=path,
                                    realEstate=listing)
                    except Exception as e:
                        print(e)
                    try:
                        newPic.save()
                    except Exception as e:
                        print(e)
        except Exception as e:
            raise


def controlFlow():
    paramObject = getParams(None)

    queryObject = makePropertyQuery(paramObject)
    if queryObject is None:
        return "Error connecting to API"

    parsedObjectList = parseHTML(queryObject[0])
    handleParsedOutput(parsedObjectList)

    for i in range(2, parsedObjectList[0]['numberOfPages'] + 1):
        paramObject = getParams(i)
        queryObject = makePropertyQuery(paramObject)
        parsedObjectList = parseHTML(queryObject[0])
        handleParsedOutput(parsedObjectList)

    return "success"


def isSameEstateByImage(propertyID):
    imgUrls = parseImageURLs(makeBaseSiteQuery(propertyID))
    images = []
    for url in imgUrls:
        image = getImage(url)
        if image is not None:
            images.append(image)

    estateIDs = EP.objects.values_list('realEstate').distinct()
    for estateID in estateIDs:
        same = []
        estatePictures = EP.objects.filter(realEstate=estateID[0])
        for estatePic in estatePictures:
            ePic = Image.open(estatePic.estatePicture)
            ePicWidth, ePicHeight = ePic.size
            imageWidth, imageHeight = images[0].size
            if (imageWidth == ePicWidth and imageHeight == ePicHeight):
                if CD(images[0], ePic) == 0:
                    for image in images:
                        image.close()
                    ePic.close()
                    return (True, estateID[0])
            ePic.close()
        if same != [] and all(same):
            return (True, estateID[0])

    return (False, images)
