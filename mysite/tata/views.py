from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    uryvky = basicInfo.objects.all()
    context = {'uryvky':uryvky}

    return render(request, 'index.html', context=context)
# Create your views here.
