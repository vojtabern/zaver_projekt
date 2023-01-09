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
from django.views.generic import ListView, DetailView, FormView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from tata.tests import Ans
from django.forms.models import model_to_dict
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet


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


class Question(ListView):
    model = Questions
    context_object_name = 'questions'
    template_name = 'questions.html'
    form_class = Ans
    initial = {'key': 'value'}
    odpovedi = []
    vyplnene = []
    kontrola = True
    answers = {}
    quest = {}

    def get_context_data(self, *args, **kwargs):
        nova = []
        question = self.model.objects.filter(test_id=self.kwargs.get('test', None)).values()
        # typ = Typ.objects.all().values()
        # print(typ)
        context = super(Question, self).get_context_data(*args, **kwargs)
        context['form'] = self.form_class(initial=self.initial)
        context['test'] = Test.objects.all().get(id=self.kwargs.get('test', None))
        context["user"] = User.objects.all().get(email=self.kwargs.get('user', None))

        context["questions"] = self.model.objects.filter(test_id=context['test'])
        AnsSet = formset_factory(Ans , extra = len(context["questions"]))
        formset = AnsSet()

        context['formset']=formset
        zabiju_se_XD = self.model.typ.through.objects.all().values()
        # print(zabiju_se_XD, "\n")
        for idx, q in enumerate(question):
            for i in zabiju_se_XD:
                if q["id"] == i["questions_id"]:
                    self.quest[idx] = {"id": q["id"], "question": q["question"], "test": q["test_id_id"], "typ":i["typ_id"]}#, "typ": q["typ_id"]
        # print("jsem v get:", self.quest)
        # print(self.quest)
        for i in self.quest:
            nova.append(self.quest[i])
        context['quest'] = nova
        return context

    def post(self, request, *args, **kwargs):

        test_id = Test.objects.all().get(id=self.kwargs.get('test', None))
        user = User.objects.get(email=self.kwargs.get('user', None))
        take = Take.objects.get(test_id=test_id, user_id=user.id)
        question = self.model.objects.filter(test_id=test_id).values()

        zabiju_se_XD = self.model.typ.through.objects.all().values()
        for idx, q in enumerate(question):
            for i in zabiju_se_XD:
                if q["id"] == i["questions_id"]:
                    self.quest[idx] = {"id": q["id"], "question": q["question"], "test": q["test_id_id"], "typ": i["typ_id"]}#, "typ": q["typ_id"]}

        AnsSet = formset_factory(Ans, extra = len(question))
        # formset = AnsSet(request.POST or None)
        my_post_dict = request.POST.copy()
        # print(my_post_dict)
        my_post_dict['form-TOTAL_FORMS'] = len(question)
        my_post_dict['form-INITIAL_FORMS'] = len(question)
        my_post_dict['form-MAX_NUM_FORMS'] = len(question)
        # print("Po zmene:\n", my_post_dict)
        myformset = AnsSet(my_post_dict)

        if myformset.is_valid() and request.method == 'POST':
            for idx, form in enumerate(myformset):

                answer = form.cleaned_data.get('answer')
                self.answers[idx] = {"q": self.quest[idx]["id"], "t": self.quest[idx]["test"],
                                     "answer": answer, "typ": self.quest[idx]["typ"]}
                ans = Answers(question_id_id=self.quest[idx]["id"] , test_id_id=self.quest[idx]["test"], value=answer)
                ans.save()

                kokos = Answers.objects.filter(question_id_id=self.quest[idx]["id"],
                                               test_id_id=self.quest[idx]["test"]).values()

                ans_take = TakeAnswers(take_id_id=take.id, questions_id_id=self.quest[idx]["id"], answer_id_id=kokos[0]["id"])
                ans_take.save()
            # print("Ans ", self.answers)
            return redirect('vyhodnoceni', test=test_id.id, user=user, result=test_id)
        else:
            return HttpResponseRedirect(request.path_info)

class Results(ListView):
    model = Answers
    template_name = 'results.html'
    context_object_name = 'answers'

    def get_context_data(self, *args, **kwargs):

        take = []
        typ = []
        take.clear()
        valid = []
        #prozatimne

        context = {
            "test": self.kwargs.get('test', None),
            "user": User.objects.get(email=self.kwargs.get('user', None)).id,
            #musim dodelat take a kotrolovat i skrz nej

        }
        context["answers"] = self.model.objects.filter(test_id=context['test'])
        taken = Take.objects.get(test_id_id=context["test"], user_id_id=context['user'])
        # print(context["answers"].values()[0]["question_id_id"])
        zabiju_se_XD = Questions.typ.through.objects.all().values()
        for idx, q in enumerate(Questions.objects.filter(test_id_id=context['test'])):
            for i in zabiju_se_XD:
                if q.id == i["questions_id"]:
                    typ.append({"typ_id": Typ.objects.filter(id=i["typ_id"]).values()[0]["id"], "que_id": q.id})
            # print(context["answers"].values()[idx]["id"])
            # print(q.id)
            # print(q.id)

            # questions.append(Questions.objects.filter(id=context["answers"].values()[idx]["question_id_id"]))
            take.append(TakeAnswers.objects.filter(answer_id_id=context["answers"].values()[idx]["id"], take_id_id=taken))
        # print(take)
        # print(typ)
        # {1: +6}
        typy = Typ.objects.all().values()
        print(take[0][0].answer_id_id)
        camyduh = {}
        for x in zabiju_se_XD:
            for i in typy:
                camyduh.update({i["id"]: 0})
                if i["id"] == x["typ_id"] and i["typ"] != 'výplňová':
                    print(i["id"])
        for i in typ:
            for idx, q in enumerate(Questions.objects.all()):
                if q.id == i["que_id"]:
                    # print("==", q.id)
                    if q.id == \
                        self.model.objects.get(question_id_id=q.id,
                                                   takeanswers=TakeAnswers.objects.get(answer_id_id=context["answers"].values()[idx]["id"], take_id_id=taken).id).question_id_id:
                            if i["typ_id"] in camyduh and camyduh[i["typ_id"]] != 0:
                                # print("co", camyduh[i["typ_id"]])
                                temp = {i["typ_id"]: camyduh[i["typ_id"]] + self.model.objects.filter(question_id_id=q.id).values()[0]["value"]}
                                print(temp)
                                camyduh.update(temp)
                            else:
                                camyduh[i["typ_id"]] = self.model.objects.filter(question_id_id=q.id).values()[0]["value"]
        print(camyduh)

        context["questions"] = Questions.objects.all()
        context["take"] = taken
        context["ansTake"] = take
        context["typ"] = typ
        context["spracuj"] = camyduh
        return context




