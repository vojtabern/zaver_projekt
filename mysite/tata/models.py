from django.db import models


class basicInfo(models.Model):
    uryvek = models.TextField(default='')
    class Meta:
        ordering = ["uryvek"]

    def __str__(self):
        return self.uryvek


# tady class
# Create your models here.
