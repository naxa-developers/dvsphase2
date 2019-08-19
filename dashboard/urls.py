
from django.contrib import admin
from django.urls import path,include
from dashboard import views


urlpatterns = [
    path('upload/',views.uploadData,name='upload'),
    path('fivew/', views.Fivew.as_view(),name='fivew'),

]
