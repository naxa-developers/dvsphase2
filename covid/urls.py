from django.urls import path
from covid import views

urlpatterns = [
    path('covid-fivew/', views.TtmpViewSet.as_view({'get': 'list'}), name='covid_fivew'),

]
