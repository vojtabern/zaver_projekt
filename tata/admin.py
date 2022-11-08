from django.contrib import admin

from . models import *

admin.site.register(Psycholog)
admin.site.register(basicInfo)
admin.site.register(Vzdelani)
admin.site.register(Client)
admin.site.register(User)
admin.site.register(Take)
admin.site.register(Test)

# Register your models here.
