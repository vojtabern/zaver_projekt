from django.urls import path

from tata.views import *
from .views import contactView, successView

urlpatterns = [
    path('async/', Uryvky.as_view(), name='index'),
    path('', Index.as_view(), name='index'),
    path('zivotopis/', Zivotopis.as_view(), name='vzdelani'),
    path('sluzby/', Sluzby.as_view(), name='sluzby'),
    path('kontakt/', contactView, name='kontakt'),
    path('success/', successView, name='success')
]