from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from realtorApp.queryMaker import controlFlow
from realtorApp.models import RealEstate as RE
from realtorApp.models import EstatePictures as EP


def index(request):
    estates_list = RE.objects.all()
    totalNumber = len(estates_list)
    paginator = Paginator(estates_list, 25)
    page = request.GET.get('page')

    try:
        estates = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        estates = paginator.page(1)
    except EmptyPage:
        estates = paginator.page(paginator.num_pages)
    return render(request, 'portfolio.html', {'estates': estates,
                                              'totalNumber': totalNumber})


def update(request):
    status = 500
    output = ""
    try:
        output = controlFlow()
    except Exception as e:
        print("error")
        print(e.message, type(e))
        status = 500
    else:
        status = 200
    finally:
        print(output)
        return HttpResponse(status=status)


def test(request):
    print("Testing")
    return HttpResponse(status=201)


def viewSingleProperty(request, id):
    try:
        re = RE.objects.get(pk=id)
        ep = EP.objects.filter(realEstate=re)
    except RE.DoesNotExist:
        return HttpResponse(status=404)
    except EP.DoesNotExist:
        ep = None

    return render(request, 'singleProperty.html', {'estates': re,
                                                   'estatePics': ep})
