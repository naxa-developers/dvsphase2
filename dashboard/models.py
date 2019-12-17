from django.contrib.gis.db import models
from django.contrib.auth.models import User
from core.models import Partner, Program, Project


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='ProfilePartner', null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='ProfileProgram', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ProfileProject', null=True, blank=True)
    image = models.ImageField(upload_to='upload/profile/', null=True, blank=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    message = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='UserProfile', null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.message
