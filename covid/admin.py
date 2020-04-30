from django.contrib import admin
from .models import CovidFivew, DryDshosp4hrSums, DryDshosp4hrUncoveredAdm1Sums, DryDshosp8hrSums, \
    DryDshosp8hrUncoveredAdm1Sums, DryDshosp12hrSums, DryDshosp12hrUncoveredAdm1Sums, DryAllCovidsDhfs4hrSums, \
    DryAllCovidsDhfs4hrUncoveredAdm1Sums, DryAllCovidsDhfs8hrSums, DryAllCovidsDhfs8hrUncoveredAdm1Sums, \
    DryAllCovidsDhfs12hrSums, DryAllCovidsDhfs12hrUncoveredAdm1Sums, CovidSpecificProgram

# Register your models here.

admin.site.register(CovidFivew)
admin.site.register(CovidSpecificProgram)
admin.site.register(DryDshosp4hrSums)
admin.site.register(DryDshosp4hrUncoveredAdm1Sums)
admin.site.register(DryDshosp8hrSums)
admin.site.register(DryDshosp8hrUncoveredAdm1Sums)
admin.site.register(DryDshosp12hrSums)
admin.site.register(DryDshosp12hrUncoveredAdm1Sums)
admin.site.register(DryAllCovidsDhfs4hrSums)
admin.site.register(DryAllCovidsDhfs4hrUncoveredAdm1Sums)
admin.site.register(DryAllCovidsDhfs8hrSums)
admin.site.register(DryAllCovidsDhfs8hrUncoveredAdm1Sums)
admin.site.register(DryAllCovidsDhfs12hrSums)
admin.site.register(DryAllCovidsDhfs12hrUncoveredAdm1Sums)
