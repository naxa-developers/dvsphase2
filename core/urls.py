from django.urls import path, include
from core import views

urlpatterns = [
    path('partner/', views.PartnerView.as_view({'get': 'list'}), name='partner'),
    path('marker-category/', views.MarkerCategoryApi.as_view({'get': 'list'}), name='marker-category'),
    path('marker-value/', views.MarkerValueApi.as_view({'get': 'list'}), name='marker-value'),
    path('district/', views.DistrictApi.as_view({'get': 'list'}), name='district'),
    path('province/', views.ProvinceApi.as_view({'get': 'list'}), name='province'),
    path('municipality/', views.GapaNapaApi.as_view({'get': 'list'}), name='municipality'),
    path('fivew/', views.Fivew.as_view({'get': 'list'}), name='fivew'),
    path('fivew-district/', views.FiveWDistrict.as_view({'get': 'list'}), name='fivew-district'),
    path('fivew-province/', views.FiveWProvince.as_view({'get': 'list'}), name='fivew-province'),
    path('fivew-municipality/', views.FiveWMunicipality.as_view({'get': 'list'}), name='fivew-municipality'),
    path('contract-sum/', views.ContractSum.as_view({'get': 'list'}), name='contract-sum'),
    path('indicator-list/', views.IndicatorApi.as_view({'get': 'list'}), name='indicator-list'),
    path('municipality-indicator/', views.IndicatorData.as_view({'get': 'list'}), name='municipality-indicator'),
    path('sector/', views.SectorApi.as_view({'get': 'list'}), name='sector'),
    path('output/', views.OutputApi.as_view({'get': 'list'}), name='output'),
    path('sub-sector/', views.SubsectorApi.as_view({'get': 'list'}), name='sub-sector'),
    path('program/', views.ProgramTestApi.as_view({'get': 'list'}), name='program'),
    path('project/', views.ProjectApi.as_view({'get': 'list'}), name='project'),
    path('travel-time/', views.TravelTimeApi.as_view({'get': 'list'}), name='travel-time'),
    path('notification/', views.NotifyApi.as_view({'get': 'list'}), name='notification'),
    path('map-layer/', views.GisApi.as_view({'get': 'list'}), name='map-layer'),
    path('district-indicator/<int:indicator_id>/', views.DistrictIndicator.as_view({'get': 'list'}),
         name="district-indicator"),
    path('province-indicator/<int:indicator_id>/', views.ProvinceIndicator.as_view({'get': 'list'}),
         name="province-indicator"),

]
