from django.db import models


class User(models.Model):
    description = "User"
    id_user = models.IntegerField(default=1, primary_key=True)

    def __str__(self):
        return self.description


class Psycholog(models.Model):
    id_psycholog = models.IntegerField(default=1, primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=50)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username


class Vzdelani(models.Model):
    OPTIONS = (
        ('základní vzdělání', 'základní vzdělání'),
        ('Psychoterapeutický výcvik', 'Psychoterapeutický výcvik'),
        ('Doplňkové vzdělání', 'Doplňkové vzdělání'),
        ('Diagnostika', 'Diagnostika'),
        ('Pracovní zkušenosti', 'Pracovní zkušenosti'),
        ('Výzkum a teoretické práce', 'Výzkum a teoretické práce'),
    )
    nazev = models.CharField(max_length=200)
    typ = models.CharField(max_length=45, choices=OPTIONS, default='základní vzdělání')
    psycholog = models.ForeignKey(Psycholog, on_delete=models.CASCADE, default=1)

    def get_options(self):
        vrat = (zakl, psycho, dopln, dia, prace, vyzkum) = self.OPTIONS
        ifo = (vrat[0][0], vrat[1][0], vrat[2][0], vrat[3][0], vrat[4][0], vrat[5][0])
        return ifo

    class Meta:
        ordering = ["typ"]

    def __str__(self):
        return self.nazev

#nefunguje why??
class Client(models.Model):
    id_client = models.IntegerField(default=1, primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["id_client"]

    def __str__(self):
        return self.id_client


class basicInfo(models.Model):
    description = "Zakl. info"
    id_basicInfo = models.IntegerField(default=1, primary_key=True)
    provozovna = models.CharField(default='Hradecká 16, Opava',max_length=200)
    telefon = models.CharField(default='+420 737 881 112',max_length=18)
    email = models.EmailField(default='jbernard@hotmail.cz')
    psycholog_id = models.OneToOneField(Psycholog, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.description

    def get_info(self):
        default = (self._meta.get_field('provozovna').get_default(), self._meta.get_field('telefon').get_default(), self._meta.get_field('email').get_default())

        return default


class Test(models.Model):
    id_test = models.IntegerField(default=1, primary_key=True)
    title = models.CharField(max_length=50, null=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Take(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, default=1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["test_id"]

    def __str__(self):
        return self.test_id

# tady class
# Create your models here.
#def get_options() -> Vzdelani.OPTIONS:
    # Get value from choices enum
    #return Vzdelani.OPTIONS