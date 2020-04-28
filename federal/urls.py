from django.urls import path, include
from federal import views
from rest_framework_mvt.views import mvt_view_factory
from .models import ProvinceBoundary, DistrictBoundary, GapaNapaBoundary

urlpatterns = [
    path('update/', views.update_boundary, name='update'),
    path("province.mvt/", mvt_view_factory(ProvinceBoundary), name='province'),
    path("district.mvt/", mvt_view_factory(DistrictBoundary), name='district'),
    path("municipality.mvt/", mvt_view_factory(GapaNapaBoundary), name='municipality'),

]
