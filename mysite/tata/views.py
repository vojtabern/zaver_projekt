import random
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
import aiohttp
from bs4 import BeautifulSoup #scraping
import requests

class Index(View):

    def get(self, request):

        informace = basicInfo.objects.all()
        num_info = basicInfo.objects.all().count()
        default = basicInfo.get_info(basicInfo)
        # uryvek = (Scrape.scrape_uryvky(Scrape, "uryvek"))
        # autor = (Scrape.scrape_uryvky(Scrape, "autor"))
        #mozna = Scrape.get_data(Scrape)
        context = {
            'informace':informace,
            'default':default,
            'num_info':num_info,
            # 'uryvek':uryvek,
            # 'autor':autor,
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
        # uryvek = Scrape.scrape_uryvky(Scrape, "uryvek")
        # autor = Scrape.scrape_uryvky(Scrape, "autor")
        context = {
            'informace': informace,
            'default': default,
            # 'uryvek': uryvek,
            # 'autor': autor,
        }
        return render(request, 'sluzby.html', context=context)

async def scrape_uryvky(request):
    #https://www.goodreads.com/api
    URL = 'https://zenquotes.io/api/quotes/authors'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            data = await res.json()
            for d in range(len(data)):
                i = d
            print(data[0]["q"])
            rand = random.randrange(0, i)
        context = {
            "quote": data[rand]["q"],
            "autor": data[rand]["a"],
        }
    return render(request, "index.html", context=context,)

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


# async def index(request):
#     # task1 = asyncio.ensure_future(Scrape.scrape_uryvky(Scrape, "autor"))
#     # task2 = asyncio.ensure_future(Scrape.scrape_uryvky(Scrape, "uryvek"))
#     await asyncio.gather(Scrape.scrape_uryvky(Scrape, "autor"), Scrape.scrape_uryvky(Scrape, "uryvek"))
#     return HttpResponse("e")
    # informace = basicInfo.objects.all()
    # num_info = basicInfo.objects.all().count()
    # default = basicInfo.get_info(basicInfo)
    # uryvek = (Scrape.scrape_uryvky(Scrape, "uryvek"))
    # autor = (Scrape.scrape_uryvky(Scrape, "autor"))
    # #mozna = sync_to_sync(Scrape.get_data(Scrape), thread_sensitive=False)
    # context = {
    #     #'mozna': mozna,
    #     'informace':informace,
    #     'default':default,
    #     'num_info':num_info,
    #     'uryvek':uryvek,
    #     'autor':autor,
    # }
    #
    # return render(request, 'index.html', context=context)