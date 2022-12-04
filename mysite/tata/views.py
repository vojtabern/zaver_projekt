import random, time
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .models import *
import aiohttp
from bs4 import BeautifulSoup #scraping
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



class Index(View):
    def get(self, request):
        context = {
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
        context = {
        }
        return render(request, 'sluzby.html', context=context)

from asgiref.sync import async_to_sync
class Uryvky(View):
    async def get(self, request):
        #https://www.goodreads.com/api
        starting_time = time.time()
        URL = 'https://zenquotes.io/api/quotes/authors'
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as res:
                data = await res.json()
                for d in range(len(data)):
                    i = d
                print(data[0]["q"])
                rand = random.randrange(0, i)
            #informace = await sync_to_async(basicInfo.objects.all())
            async for info in basicInfo.objects.all():
                # informace = {info.name:'name', info.surrname:'surrname', info.provozovna:'provozovna',
                #              info.telefon:'telefon', info.email:'email', info.titul:'titul'}
                informace = (info.name, info.surrname, info.provozovna,
                              info.telefon, info.email, info.titul)
            context = {
                "quote": data[rand]["q"],
                "autor": data[rand]["a"],
                "async_info": informace,
            }
        total_time = time.time() - starting_time
        print(total_time)
        return render(request, "index.html", context=context,)



# musim pres api
def contactView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            email = form.cleaned_data["from_email"]
            from_email = "gridsend.kontakt@gmail.com"
            to_email = "vojtabern@gmail.com"
            text = form.cleaned_data['message']
            subject = subject + ' || mail: ' + email
            message = Mail(
                from_email, to_email, subject, text
            )
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            return redirect("success")
    return render(request, "contact.html", {"form": form})

def successView(request):
    return HttpResponse("Success! Thank you for your message.")



# Create your views here.

