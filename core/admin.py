from django.contrib import admin
from .models import Partner,Program,Sector,SubSector,MarkerCategory,MarkerValues
# Register your models here.

admin.site.register(Partner)
admin.site.register(Program)
admin.site.register(Sector)
admin.site.register(SubSector)
admin.site.register(MarkerCategory)
admin.site.register(MarkerValues)
