from django.shortcuts import render
from .models import ProvinceBoundary


# Create your views here.
def update_boundary(request):
    province_data = ProvinceBoundary.objects.all()
    print('data', province_data)
