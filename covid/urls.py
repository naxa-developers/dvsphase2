from django.urls import path
from covid import views

urlpatterns = [
    path('covid-fivew/', views.TtmpViewSet.as_view({'get': 'list'}), name='covid-fivew'),

    path('dry-deshosp-4hr-sums/', views.DryDshosp4hrSumsViewSet.as_view({'get': 'list'}), name='dry-deshosp-4hr-sums'),
    path('dry-deshosp-4hr-uncovered-adm1/', views.DryDshosp4hrUncoveredAdm1SumsViewSet.as_view({'get': 'list'}),
         name='dry-deshosp-4hr-uncovered-adm1'),
    path('dry-deshosp-8hr-sums/', views.DryDshosp8hrSumsViewSet.as_view({'get': 'list'}), name='dry-deshosp-8hr-sums'),
    path('dry-deshosp-8hr-uncovered-adm1/', views.DryDshosp8hrUncoveredAdm1SumsViewSet.as_view({'get': 'list'}),
         name='dry-deshosp-8hr-uncovered-adm1'),
    path('dry-deshosp-12hr-sums/', views.DryDshosp12hrSumsViewSet.as_view({'get': 'list'}),
         name='dry-deshosp-12hr-sums'),
    path('dry-deshosp-12hr-uncovered-adm1/', views.DryDshosp12hrUncoveredAdm1SumsViewSet.as_view({'get': 'list'}),
         name='dry-deshosp-12hr-uncovered-adm1'),
    path('dry-allcovidhfs-4hr-sums/', views.DryAllCovidsDhfs4hrSumsViewSet.as_view({'get': 'list'}),
         name='dry-allcovidhfs-4hr-sums'),
    path('dry-allcovidhfs-4hr-uncovered-adm1/',
         views.DryAllCovidsDhfs4hrUncoveredAdm1SumsViewSet.as_view({'get': 'list'}),
         name='dry-allcovidhfs-4hr-uncovered-adm1'),
    path('dry-allcovidhfs-8hr-sums/', views.DryAllCovidsDhfs8hrSumsViewSet.as_view({'get': 'list'}),
         name='dry-allcovidhfs-8hr-sums'),
    path('dry-allcovidhfs-8hr-uncovered-adm1/',
         views.DryAllCovidsDhfs8hrUncoveredAdm1SumsViewSet.as_view({'get': 'list'}),
         name='dry-allcovidhfs-8hr-uncovered-adm1'),
    path('dry-allcovidhfs-12hr-sums/', views.DryAllCovidsDhfs12hrSumsViewSet.as_view({'get': 'list'}),
         name='dry-allcovidhfs-12hr-sums'),
    path('dry-allcovidhfs-12hr-uncovered-adm1/',
         views.DryAllCovidsDhfs12hrUncoveredAdm1SumsViewSet.as_view({'get': 'list'}),
         name='dry-allcovidhfs-12hr-uncovered-adm1'),

]
