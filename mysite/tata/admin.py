from django.contrib import admin

from . models import *

admin.site.register(Psycholog)
admin.site.register(basicInfo)
admin.site.register(Vzdelani)
admin.site.register(Client)
admin.site.register(User)
admin.site.register(Take)
admin.site.register(Test)
admin.site.register(Answers)
admin.site.register(Questions)
admin.site.register(TakeAnswers)


# Register your models here.
