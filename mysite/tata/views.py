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
from tata.tests import Ans, Formset
from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory
from django.core.exceptions import ValidationError

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
        context['quest'] = Questions.objects.filter(test_id=self.kwargs["pk"]).values()[:1]
        tmp = context['quest'][0]
        context['quest'] = tmp
        context['user'] = User.objects.get(email=self.kwargs.get('user', None))
        return context

# class Question(ListView):
#     model = Questions
#     context_object_name = 'questions'
#     template_name = 'questions.html'
#     form_class = Ans
#     initial = {'key': 'value'}
#     odpovedi = []
#     kontrola = True

class Question(ListView):
    model = Questions
    context_object_name = 'questions'
    template_name = 'questions.html'
    form_class = formset_factory(Ans, formset=Formset)
    initial = {'key': 'value'}
    odpovedi = []
    vyplnene = []
    kontrola = True

    def get_context_data(self, *args, **kwargs):


        context = super(Question, self).get_context_data(*args, **kwargs)
        context["questions"] = self.model.objects.filter(test_id=self.kwargs.get('test', None))
        context['test'] = Test.objects.all().get(id=self.kwargs.get('test', None))
        context['form'] = self.form_class()

        return context


        question = self.model.objects.filter(test_id=self.kwargs.get('test', None)).values()
        context['form'] = self.form_class(initial=self.initial)
        context['test'] = Test.objects.all().get(id=self.kwargs.get('test', None))
        context["user"] = User.objects.all().get(email=self.kwargs.get('user', None))


        i = self.request.session.get('i', 0)
        print("V get je I: ", i)
        if i < len(question):
            context['question'] = self.model.objects.get(id=question[i]["id"])
            context['button'] = "Další otázka"
            print("Tohle je novy question: ", context["question"])
            return context
        else:
            context['button'] = "Ukaž výsledky"
            return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            try:
                delblogformset = self.form_class(request.POST)
            except ValidationError:
                delblogformset = None
            if delblogformset and delblogformset.is_valid():

                return HttpResponseRedirect('/home')
        # context = super(Question, self.get_context_data(*args, **kwargs)).get_context_data(*args, **kwargs)
        # print(context["questions"])
        test_id = Test.objects.all().get(id=self.kwargs.get('test', None))
        user = User.objects.get(email=self.kwargs.get('user', None))
        take = Take.objects.get(test_id=test_id, user_id=user.id)
        question = self.model.objects.filter(test_id=test_id).values()
        i = request.session.get('i', 0)
        if i < len(question):
            request.session["i"] = i + 1
        else:
            print("i je: ", i)
            request.session["i"] = 0
            #mazani uzivatele
            User.objects.get(email=user).delete()

            return redirect('vyhodnoceni', test=test_id.id, user=self.kwargs.get('user', None), result=test_id.title)
        print("user: ", user)
        print("take: ", take)
        print( " index: ", i)
        print("question: ", question[i]["id"])
        # print(TakeAnswers.objects.filter(take_id=take.id, question_id=, answer_id=))
        if form.is_valid():
            answer = form.cleaned_data['answer']
            print("answer: ", answer)
            self.odpovedi.append({"id_qu":question[i]["id"], "question": question[i]["question"], "value": answer})
            print(self.odpovedi)
            return redirect('question', test=test_id.id, user=User.objects.get(email=self.kwargs.get('user', None)),
                            pk=question[i]["id"])


class Results(View):
    answers = Question.odpovedi
    del Question.odpovedi[0:len(Question.odpovedi)]
    def get(self, request, **kwargs):
        #prozatimne
        context = {
            "test": self.kwargs.get('test', None),
            "user": self.kwargs.get('user', None),
            "answers": self.answers,
        }
        return render(request, 'results.html', context=context)


