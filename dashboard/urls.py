from django.contrib import admin
from django.urls import path, include
from dashboard import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('upload/', views.uploadData, name='upload'),
    path('upload-shapefile/', views.ShapefileUpload, name='upload-shapefile'),

    path('invitation/', views.Invitation, name='invitation'),
    path('login-test/', views.login_test, name='login-test'),
    path('logout/', auth_views.logout, {'next_page': '/dashboard/login/'}, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.login, name='login'),
    path('check-login/', views.check_login, name='check-login'),
    path('token/', views.auth, name='token'),
    path('main/', views.Dashboard.as_view(), name='main'),

    path('page_province/', views.province_list, name='page_province'),

    path('program-list/', views.ProgramList.as_view(), name='program-list'),
    path('program-add/', views.ProgramCreate.as_view(), name='program-add'),
    path('program-edit/<int:pk>', views.ProgramUpdate.as_view(), name='program-edit'),
    path('program-delete/<int:pk>', views.ProgramDelete.as_view(), name='program-delete'),

    path('partner-list/', views.PartnerList.as_view(), name='partner-list'),
    path('partner-add/', views.PartnerCreate.as_view(), name='partner-add'),
    path('partner-edit/<int:pk>', views.PartnerUpdate.as_view(), name='partner-edit'),
    path('partner-delete/<int:pk>', views.PartnerDelete.as_view(), name='partner-delete'),

    path('sector-list/', views.SectorList.as_view(), name='sector-list'),
    path('sector-add/', views.SectorCreate.as_view(), name='sector-add'),
    path('sector-edit/<int:pk>', views.SectorUpdate.as_view(), name='sector-edit'),
    path('sector-delete/<int:pk>', views.SectorDelete.as_view(), name='sector-delete'),

    path('subsector-list/', views.SubSectorList.as_view(), name='subsector-list'),

    path('marker-list/', views.MarkerList.as_view(), name='marker-list'),
    path('markervalue-list/', views.MarkerValueList.as_view(), name='markervalue-list'),

    path('indicator-list/', views.IndicatorList.as_view(), name='indicator-list'),
    path('indicator-data/', views.IndicatorValueList.as_view(), name='indicator-data'),
    # path('program-list/', views.ProgramList.as_view(), name='program-list'),








]
