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
    path('page_program/', views.ProgramList.as_view(), name='page_program'),
    path('login/', auth_views.login, name='login'),
    path('main/', views.Dashboard.as_view(), name='main'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.logout, {'next_page': '/dashboard/login/'}, name='logout'),




]
