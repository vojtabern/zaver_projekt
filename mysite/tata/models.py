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


class Vzdelani(models.Model):
    OPTIONS = (
        ('základní vzdělání','základní vzdělání'),
        ('Psychoterapeutický výcvik','Psychoterapeutický výcvik'),
        ('Doplňkové vzdělání', 'Doplňkové vzdělání'),
        ('Diagnostika', 'Diagnostika'),
        ('Pracovní zkušenosti','Pracovní zkušenosti'),
        ('Výzkum a teoretické práce','Výzkum a teoretické práce'),
    )
    nazev = models.CharField( max_length=200)
    typ = models.CharField(max_length=45, choices=OPTIONS, default='základní vzdělání')



    class Meta:
        ordering = ["typ"]

    def __str__(self):
        return self.nazev

# tady class
# Create your models here.
#def get_options() -> Vzdelani.OPTIONS:
    # Get value from choices enum
    #return Vzdelani.OPTIONS