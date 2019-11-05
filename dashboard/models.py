from django.contrib.gis.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)


class Log(models.Model):
    message = models.CharField(max_length=300, null=True, blank=True)
    user = models.CharField(max_length=300, null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.message
