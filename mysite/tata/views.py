from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):

    informace = basicInfo.objects.all()
    num_info = basicInfo.objects.all().count()
    default_pro = basicInfo._meta.get_field('provozovna').get_default()
    default_tel = basicInfo._meta.get_field('telefon').get_default()
    default_email = basicInfo._meta.get_field('email').get_default()
    context = {
        'informace':informace,
        'num_info':num_info,
        'default_pro': default_pro,
        'default_tel': default_tel,
        'default_email': default_email
    }

    return render(request, 'index.html', context=context)


def vzdelani(request):
    #y = Vzdelani.objects.all()
    #grad = all(x.OPTIONS for x in y)
    typ = Vzdelani.typ
    num_vzde = Vzdelani.objects.all().count()
    vzdelani_vse = Vzdelani.objects.all()
    vse = []
    for i in range(0, num_vzde):
        vse.append(i)

    vzdelani = Vzdelani.objects.filter(typ='základní vzdělání').values()
    vzdelani1 = Vzdelani.objects.filter(typ='Psychoterapeutický výcvik').values()
    vzdelani2 = Vzdelani.objects.filter(typ='Doplňkové vzdělání').values()
    vzdelani3 = Vzdelani.objects.filter(typ='základní vzdělání').values()
    vzdelani4 = Vzdelani.objects.filter(typ='Pracovní zkušenosti').values()
    vzdelani5 = Vzdelani.objects.filter(typ='Výzkum a teoretické práce').values()

    context = {
        'daty':vzdelani_vse,
        'vzdelani0':vzdelani,
        'vzdelani1':vzdelani1,
        'vzdelani2': vzdelani2,
        'vzdelani3': vzdelani3,
        'vzdelani4': vzdelani4,
        'vzdelani5':vzdelani5,
        'vse':vse,
    }
    return render(request, 'vzdelani.html', context=context)

# Create your views here.
