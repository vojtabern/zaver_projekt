from django.urls import path

from tata.views import *
from .views import MyFormView

urlpatterns = [
    # path('async/', Uryvky.as_view(), name='index'),
    path('', Index.as_view(), name='index'),
    path('zivotopis/', Zivotopis.as_view(), name='vzdelani'),
    path('sluzby/', Sluzby.as_view(), name='sluzby'),
    path('kontakt/', MyFormView.as_view(), name='kontakt'),
    path('firmy/', Firmy.as_view(), name='firmy'),
    path('success/', MyFormView.as_view(), name='success'),
    path('testy/', TestListView.as_view(), name='testy'),
    path('testy/<int:pk>/<user>', TestDetail.as_view(), name='test'),
    path('testy/<int:pk>/<user>/<question>', Question.as_view(), name='question'),

]