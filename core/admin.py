from django.contrib import admin
from .models import Partner, Program, Sector, SubSector, MarkerCategory, MarkerValues, Province, District, GapaNapa, \
    FiveW, Indicator, IndicatorValue, TravelTime, GisLayer, Project, PartnerContact, Output, ProvinceDummy, \
    Notification, BudgetToSecondTier, BudgetToFirstTier, Cmp, Filter, GisStyle, GisPop, NepalSummary, FeedbackForm,FAQ,TermsAndCondition,NationalStatistic

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
admin.site.register(Indicator)
admin.site.register(IndicatorValue)
admin.site.register(TravelTime)
admin.site.register(GisLayer)
admin.site.register(Project)
admin.site.register(PartnerContact)
admin.site.register(Output)
admin.site.register(ProvinceDummy)
admin.site.register(Notification)
admin.site.register(BudgetToSecondTier)
admin.site.register(BudgetToFirstTier)
admin.site.register(Cmp)
admin.site.register(Filter)
admin.site.register(GisStyle)
admin.site.register(GisPop)
admin.site.register(NepalSummary)
admin.site.register(FeedbackForm)
admin.site.register(FAQ)
admin.site.register(TermsAndCondition)
admin.site.register(NationalStatistic)