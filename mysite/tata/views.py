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
# Create your views here.
