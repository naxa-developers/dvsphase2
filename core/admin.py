from django.contrib import admin
from .models import Partner, Program, Sector, SubSector, MarkerCategory, MarkerValues, Province, District, GapaNapa, \
    FiveW

# Register your models here.

admin.site.register(Partner)
admin.site.register(Program)
admin.site.register(Sector)
admin.site.register(SubSector)
admin.site.register(MarkerCategory)
admin.site.register(MarkerValues)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(GapaNapa)
admin.site.register(FiveW)
