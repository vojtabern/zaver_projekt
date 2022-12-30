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
    context_object_name = 'questions'
    template_name = 'questions.html'
    form_class = Ans
    initial = {'key': 'value'}
    odpovedi = []

    def get_context_data(self,*args, **kwargs):
        mozne = []
        context = super(Question, self).get_context_data(*args, **kwargs)
        context['form'] = self.form_class(initial=self.initial)
        context['test'] = Test.objects.all().get(id=self.kwargs.get('test', None))
        context["user"] = User.objects.all().get(email=self.kwargs.get('user', None))
        #jestli se TEst.id = question.test_id tak chci zobrazit otázku.
        mozne.append(self.model.objects.filter(test_id=context["test"].id).values())
        print("user id: ", context["user"].id)
        for j in mozne:
            for q in j:
                if q["test_id_id"] == context['test'].id and q["id"] != context["questions"].id:
                    context["mozne"] = q["id"]
        # print(mozne)
        if context['test'].id == context["questions"].test_id_id:
            # print(context["questions"].id)
            context["question"] = context["questions"]
            # print(context["question"])
            return context
        else:
            context["question"] = "Daná otázka pro daný test neexituje"
        return context

        # if context['test'] ==
        # context['question'] = self.model.objects.all().get(test_id=self.kwargs.get('test', None), id=self.kwargs["pk"])
        # otazky.append(self.model.objects.filter(test_id=self.kwargs.get('test', None)).values())
        # print(otazky)
        # for i in otazky:
        #     for j in range(len(i)):
        #         mozne.append(i[j]["id"])
        # print(mozne)
        # context['question'] = otazky
        # context["next_q_id"] = mozne
        # print(self.model.objects.all().filter(test_id=self.kwargs.get('test', None)))
    def post(self, request, *args, **kwargs):
        mozne = []
        form = self.form_class(request.POST)
        test_id = Test.objects.all().get(id=self.kwargs.get('test', None))
        vyplnene = {}
        i = request.session.get('i', 0)
        if form.is_valid():
            mozne.append(self.model.objects.filter(test_id=test_id).values())
            for j in mozne:
                for q in j:
                    # print(q["id"] , "==" , self.model.objects.get(id=self.kwargs.get('pk', None)).id)
                    if i > 0:
                        if q["test_id_id"] == test_id.id and q["id"] != self.model.objects.get(id=self.kwargs.get('pk', None)).id:

                            mozne = q["id"]
                            request.session["vyplnene"] = q["id"]
                            print(self.odpovedi)
                    else:
                        if q["test_id_id"] == test_id.id and q["id"] != self.model.objects.get(id=self.kwargs.get('pk', None)).id:
                            mozne = q["id"]
                            request.session["vyplnene"] = q["id"]
            # print(mozne)
            # odsud beru data a ukladam je do self.odpovedi
            request.session["i"] = i + 1
            vyplnene["otazka"] = self.kwargs.get("pk", None)
            answer = form.cleaned_data['answer']
            uzivatel = request.session["user"] = User.objects.get(email=self.kwargs.get("user", None)).id
            kokosak = request.session["ans"] = answer
            vyplnene["user"] = uzivatel
            vyplnene["odpoved"] = kokosak
            self.odpovedi.append(vyplnene)
            #pocamcad

            print(self.odpovedi)
            print(uzivatel, " ", kokosak)
            return redirect('question', test=test_id.id, user=User.objects.get(email=self.kwargs.get('user', None)), pk=mozne)
        else:
            form = Ans()
            return redirect('question', test=test_id.id, user=User.objects.get(email=self.kwargs.get('user', None)),
                            pk=self.model.objects.id)
        # return redirect('question', pk=mozne)

        # def get_context_data(self, **kwargs):
        #     context = super(Question, self).get_context_data(**kwargs)
        #     # Create any data and add it to the context
        #     context['test'] = Take.objects.all().filter(test_id=self.kwargs["pk"])
        #     # print(Take.objects.get(user_id="num"))
        #     context['user'] = Take.objects.filter(test_id=self.kwargs["pk"])
        #     # context['answer'] = Answers.objects.filter(question_id=self.kwargs["pk"], test_id=self.kwargs["pk"])
        #     # print(Take.objects.filter(test_id=self.kwargs["pk"]))
        #     return context





