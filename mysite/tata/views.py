from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *




class Index(View):
    def get(self, request):
        informace = basicInfo.objects.all()
        num_info = basicInfo.objects.all().count()
        default = basicInfo.get_info(basicInfo)
        context = {
            'informace':informace,
            'default':default,
            'num_info':num_info,
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
        ahoj = "hello world"
        context = {
            'informace': informace,
            'default': default,
            'ahoj':ahoj,
        }
        return render(request, 'sluzby.html', context=context)

# Create your views here.
