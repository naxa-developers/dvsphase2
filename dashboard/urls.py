from django.contrib import admin
from django.urls import path, include
from dashboard import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('upload/', views.uploadData, name='upload'),
    path('upload-shapefile/', views.ShapefileUpload, name='upload-shapefile'),
    path('invitation/', views.Invitation, name='invitation'),
    path('login-test/', views.login_test, name='login-test'),
    path('token/', views.auth, name='token'),
    path('check-login/', views.check_login, name='check-login'),
    path('page_province/', views.province_list, name='page_province'),
    path('program-list/', views.ProgramList.as_view(), name='program-list'),
    path('partner-list/', views.PartnerList.as_view(), name='partner-list'),
    path('sector-list/', views.SectorList.as_view(), name='sector-list'),
    path('subsector-list/', views.SubSectorList.as_view(), name='subsector-list'),
    path('marker-list/', views.MarkerList.as_view(), name='marker-list'),
    path('markervalue-list/', views.MarkerValueList.as_view(), name='markervalue-list'),
    path('indicator-list/', views.IndicatorList.as_view(), name='indicator-list'),
    path('indicator-data/', views.IndicatorValueList.as_view(), name='indicator-data'),
    # path('program-list/', views.ProgramList.as_view(), name='program-list'),
    path('login/', auth_views.login, name='login'),
    path('main/', views.Dashboard.as_view(), name='main'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.logout, {'next_page': '/dashboard/login/'}, name='logout'),




]
