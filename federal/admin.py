from django.contrib import admin
from .models import ProvinceBoundary, DistrictBoundary, GapaNapaBoundary

# Register your models here.

admin.site.register(ProvinceBoundary)
admin.site.register(DistrictBoundary)
admin.site.register(GapaNapaBoundary)
