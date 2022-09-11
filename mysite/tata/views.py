import random

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from tata.quotes import Scrape



class Index(View):
    def get(self, request):
        informace = basicInfo.objects.all()
        num_info = basicInfo.objects.all().count()
        default = basicInfo.get_info(basicInfo)
        uryvek = Scrape.scrape_uryvky(Scrape, "uryvek")
        autor = Scrape.scrape_uryvky(Scrape, "autor")

        context = {
            'informace':informace,
            'default':default,
            'num_info':num_info,
            'uryvek':uryvek,
            'autor':autor,
        }

        return render(request, 'index.html', context=context)


class Zivotopis(View):
    def get(self, request):
        vrat = Vzdelani.get_options(Vzdelani)
        vzdelani = Vzdelani.objects.all()

        context = {
            'vrat':vrat,
            'vzdelani': vzdelani,
        }
        return render(request, 'vzdelani.html', context=context)

class Sluzby(View):

    def get(self, request):
        informace = basicInfo.objects.all()
        default = basicInfo.get_info(basicInfo)
        uryvek = Scrape.scrape_uryvky(Scrape, "uryvek")
        autor = Scrape.scrape_uryvky(Scrape, "autor")
        context = {
            'informace': informace,
            'default': default,
            'uryvek': uryvek,
            'autor': autor,
        }
        return render(request, 'sluzby.html', context=context)

# Create your views here.

# class Quotes(View):
#     def get(self, request):
#         n = 3
#         for num in range(0, n):
#             uryvek = Scrape.scrape_uryvky(Scrape, num)
#         ahoj = () = (uryvek[0])
#
#         context = {
#             'uryvek':ahoj,
#         }
#
#         return render(request, 'card.html', context=context)

