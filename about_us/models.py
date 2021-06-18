from django.db import models
from django.db.models.base import ModelState
from django.db.models.fields import CharField
from ckeditor.fields import RichTextField

# Create your models here.


class AboutUs(models.Model):
    title = RichTextField(blank=True, null=True)
    sub_title = RichTextField(blank=True, null=True)
    body = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'


class ContactUs(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    address = RichTextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
