import random, time

from .forms import ContactForm, User_Id
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
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from tata.tests import Ans
from django.forms.models import model_to_dict

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


class Firmy(View):
    def get(self, request):
        context = {
        }
        return render(request, 'firms.html', context=context)


class MyFormView(View):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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
                print(e.massage)
            messages.info(request, 'Email úspěšně odeslán')
            return redirect('kontakt')
        else:
            form = ContactForm()
        return redirect('kontakt')





class TestListView(ListView):
    model = Test
    form_class = User_Id
    context_object_name = 'test_list'
    template_name = 'testy.html'
    initial = {'key': 'value'}
    control = []

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        kokos = Test.objects.all().values()
        print(kokos)
        if kokos == None:
            messages.warning(request, 'Omlouváme se, ale ještě nebyly vytvořeny žádné testy')
            return redirect('test', pk=self.kwargs["pk"])
        return render(request, self.template_name, {'form': form, "test":kokos})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.num = request.POST.get("number")
        kontrola = []
        for i in User.objects.values():
            kontrola.append(i)
        for i in kontrola:
            self.control.append(i['email'])
            print(i['email'])
        if form.is_valid():
            user = form.cleaned_data['user']
            if user not in self.control:
                request.session["user"] = user
                request.session.set_expiry(60)
                u = User(email=user)
                u.save()
                test = Take(user_id=User.objects.get(email=user), test_id=Test.objects.get(pk=self.num))
                test.save()
                return redirect('test', pk=self.num, user=user)
            else:
                messages.warning(request, 'Omlouváme se, ale daný uživatel již existuje')
                return redirect('testy')
        else:
            messages.info(request, 'Nesprávně vyplněný email')
        return redirect('test', pk=self.num)


class TestDetail(DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(TestDetail, self).get_context_data(**kwargs)
        #Create any data and add it to the context
        context['num'] = Questions.objects.all().filter(test_id=self.kwargs["pk"]).count()
        # print(Take.objects.get(user_id="num"))
        context['user'] = Take.objects.filter(test_id = self.kwargs["pk"])
        # print(Take.objects.filter(test_id=self.kwargs["pk"]))
        return context


class Question(DetailView):
    model = Questions
    context_object_name = 'question'
    template_name = 'questions.html'
    form_class = Ans
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        otazky = []
        kokos = Questions.objects.all().values()


        if self.kwargs.get('pk', None) is not None:
            kokos = self.model.objects.all().filter(test_id=self.kwargs.get('pk', None)).values()
        for i in kokos:
            otazky.append(i)
        print(otazky)
        return render(request, self.template_name, {"form": form, "question": kokos,
                                                    "test": self.kwargs.get('pk', None)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            answer = form.cleaned_data['ans']
            request.session["ans"] = answer
        else:
            form = Ans()
        return render(request, self.template_name, {'form': form, 'question': self.model.objects.all()})

        # def get_context_data(self, **kwargs):
        #     context = super(Question, self).get_context_data(**kwargs)
        #     # Create any data and add it to the context
        #     context['test'] = Take.objects.all().filter(test_id=self.kwargs["pk"])
        #     # print(Take.objects.get(user_id="num"))
        #     context['user'] = Take.objects.filter(test_id=self.kwargs["pk"])
        #     # context['answer'] = Answers.objects.filter(question_id=self.kwargs["pk"], test_id=self.kwargs["pk"])
        #     # print(Take.objects.filter(test_id=self.kwargs["pk"]))
        #     return context





