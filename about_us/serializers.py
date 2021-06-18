from django.db import models
from django.db.models import fields
from .models import AboutUs, ContactUs
from rest_framework import serializers


class AboutUsSerializers(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = '__all__'


class ContactUsSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = '__all__'
