from django.urls import path, include
from rest_framework import routers
from dashboard.viewsets.dashboard_viewsets import *

router = routers.DefaultRouter()
router.register(r'partners', PartnerViewset)
router.register(r'programs', ProgramViewset)

urlpatterns = [
    path('', include(router.urls)),
]
