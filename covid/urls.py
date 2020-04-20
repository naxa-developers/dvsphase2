from django.urls import path
from covid import views

urlpatterns = [
    path('ttmp/', views.TtmpViewSet.as_view({'get': 'list'}), name='ttmp'),

]