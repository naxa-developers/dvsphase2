from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('upload/', views.uploadData, name='upload'),
    path('upload-shapefile/', views.ShapefileUpload, name='upload-shapefile'),

]
