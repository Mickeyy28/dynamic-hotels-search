from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.


def Home(request):
    emenities = Emenities.objects.all()
    context = {"emenities": emenities}
    return render(request, 'home.html', context)


def hotel_Api(request):
    hotels_objs = Hotels.objects.all()
    print(request.GET.get('price'))

    if request.GET.get('price'):
        hotels_objs = hotels_objs.filter(
            price__lte=int(request.GET.get('price')))
    print(request.GET.get('emenities'))

    if request.GET.get('emenities'):
        emenities = request.GET.get('emenities').split(',')
        em = []
        for e in emenities:
            try:
                em.append(int(e))
            except Exception as e:
                pass
        try:
            hotels_objs = hotels_objs.filter(emenities__in=(em)).distinct()
        except Exception as e:
            print(e)

    payload = []
    for hotel_obj in hotels_objs:
        result = {}
        result['hotel_name'] = hotel_obj.hotel_name
        result['hotel_description'] = hotel_obj.hotel_description
        result['price'] = hotel_obj.price
        result['hotel_image'] = hotel_obj.hotel_image
        payload.append(result)
    return JsonResponse(payload, safe=False)


def hotel_search(request):
    hotel_name = request.GET.get('hotel_name')
    payload = []
    if hotel_name:
        hotels_objs = Hotels.objects.filter(hotel_name__contains=hotel_name)
        for hotel_obj in hotels_objs:
            result = {}
            result['hotel_name'] = hotel_obj.hotel_name
            result['hotel_description'] = hotel_obj.hotel_description
            result['price'] = hotel_obj.price
            result['hotel_image'] = hotel_obj.hotel_image
            payload.append(result)
    return JsonResponse(payload, safe=False)
