from django.shortcuts import render
from django.http import HttpResponse
from realtorApp.queryMaker import controlFlow
from realtorApp.models import RealEstate as RE


def index(request):
    query_results = RE.objects.all()
    return render(request, 'base.html', {'estates': query_results})


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
