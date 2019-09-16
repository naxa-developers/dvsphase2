from django.urls import path, include
from core import views

urlpatterns = [
    path('partner/', views.PartnerView.as_view(), name='partner'),
    # path('program/', views.ProgramView.as_view(), name='program'),
    path('marker-category/', views.MarkerCategoryApi.as_view(), name='marker-category'),
    path('marker-value/', views.MarkerValueApi.as_view({'get': 'list'}), name='marker-value'),
    path('district/', views.DistrictApi.as_view(), name='district'),
    path('province/', views.ProvinceApi.as_view(), name='province'),
    path('gapanapa/', views.GapaNapaApi.as_view({'get': 'list'}), name='gapanapa'),
    path('fivew/', views.Fivew.as_view(), name='fivew'),
    path('indicator-list/', views.IndicatorApi.as_view(), name='indicator-list'),
    # path('indicator-value/', views.IndicatorValueApi.as_view(), name='indicator-value'),
    path('indicator-value/', views.IndicatorData.as_view({'get': 'list'}), name='indicator-value'),
    path('sector/', views.SectorApi.as_view({'get': 'list'}), name='sector'),
    path('sub-sector/', views.SubsectorApi.as_view({'get': 'list'}), name='sub-sector'),
    path('program/', views.ProgramTestApi.as_view({'get': 'list'}), name='program'),
    path('travel-time/', views.TravelTimeApi.as_view({'get': 'list'}), name='travel-time'),

]
