from django.urls import path

from tata.views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('zivotopis/', Zivotopis.as_view(), name='vzdelani')
]