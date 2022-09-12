from django.urls import path

from tata.views import *

urlpatterns = [
    path('async/', scrape_uryvky, name='index'),
    path('', Index.as_view(), name='index'),
    path('zivotopis/', Zivotopis.as_view(), name='vzdelani'),
    path('sluzby/', Sluzby.as_view(), name='sluzby')
]