from django.db import models


class User(models.Model):
    description = "User"
    email = models.CharField(max_length=90)

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.email


class Psycholog(models.Model):
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    psycholog = models.ForeignKey(Psycholog, on_delete=models.CASCADE)

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
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["user_id"]

    def __int__(self):
        return self.user_id


class basicInfo(models.Model):
    description = "Zakl. info"
    name = models.CharField(default='Jan',max_length=200)
    surrname = models.CharField(default='Bernard', max_length=200)
    provozovna = models.CharField(default='Hradecká 16, Opava',max_length=200)
    telefon = models.CharField(default='+420 737 881 112',max_length=18)
    email = models.EmailField(default='jbernard@hotmail.cz')
    titul = models.CharField(default='Mgr.',max_length=18)
    psycholog_id = models.OneToOneField(Psycholog, on_delete=models.CASCADE)

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.description

    def get_info(self):
        default = (self._meta.get_field('name').get_default(), self._meta.get_field('surrname').get_default(),
                   self._meta.get_field('provozovna').get_default(), self._meta.get_field('telefon').get_default(),
                   self._meta.get_field('email').get_default(), self._meta.get_field('titul').get_default())
        return default


class Test(models.Model):
    title = models.CharField(max_length=50, null=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default="Zde napište o čem tento test je")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Take(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["test_id"]

    def __int__(self):
        return self.test_id


class Questions(models.Model):
    question = models.CharField(max_length=45, default="Zde napište otázku")
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        ordering = ["question"]

    def __str__(self):
        return self.question


class Answers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        ordering = ["value"]

    def __int__(self):
        return self.value


class TakeAnswers(models.Model):
    take_id = models.ForeignKey(Take, on_delete=models.CASCADE)
    questions_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answers, on_delete=models.CASCADE)

    class Meta:
        ordering = ["take_id"]

    def __int__(self):
        return self.take_id


# tady class
# Create your models here.
#def get_options() -> Vzdelani.OPTIONS:
    # Get value from choices enum
    #return Vzdelani.OPTIONS