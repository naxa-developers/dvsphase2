from django.urls import path, include
from rest_framework import routers

from dashboard.viewsets.dashboard_viewsets import *

router = routers.DefaultRouter()
router.register(r"partners", PartnerViewset)
router.register(r"partnercontact", PartnerContactViewset)
router.register(r"programs", ProgramViewset)
router.register(r"projects", ProjectViewset)
router.register(r"fivew", FiveWViewset)
router.register(r"sector", SectorViewset)
router.register(r"sub-sector", SubSectorViewset)
router.register(r"markercategory", MarkerCategoryViewset)
router.register(r"markervalue", MarkerValueViewset)
router.register(r"indicator", IndicatorViewset)
router.register(r"province", ProvinceViewset)
router.register(r"district", DistrictViewset)
router.register(r"palika", PalikaViewset)
router.register(r"output", OutputViewset)
router.register(r"group", GroupManagementViewset)
router.register(r"user", UserViewset)
router.register(r"cmp", CmpViewset)
router.register(r"faq", FAQViewset)
router.register(r"terms", TermsAndConditionViewset)
router.register(r"about", AboutUsViewset)
router.register(r"contact", ContactViewset)
router.register(r"vector", VectorLayerViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
