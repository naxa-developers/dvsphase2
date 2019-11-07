from django.contrib import admin
from .models import UserProfile, Log

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Log)