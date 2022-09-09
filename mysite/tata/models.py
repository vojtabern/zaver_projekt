from django.db import models


class basicInfo(models.Model):
    description = "Zakl. info"
    provozovna = models.CharField(default='Hradecká 16, Opava',max_length=200)
    telefon = models.CharField(default='+420 737 881 112',max_length=18)
    email = models.EmailField(default='jbernard@hotmail.cz')

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.description


# tady class
# Create your models here.
